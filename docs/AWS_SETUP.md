# AWS Setup: S3 + Transcribe

The Video-KYC app uploads the customer's audio to Amazon S3 and transcribes it with AWS Transcribe.
This guide sets up the minimum AWS access the app needs.

---

## 1. Create an S3 bucket

1. Sign in to the AWS Console → open **S3** → **Create bucket**.
2. **Bucket name:** for example `my-vkyc-audio-bucket` (must be globally unique).
3. **Region:** `ap-south-1` (Mumbai) or your preferred region.
4. **Block Public Access:** keep **all** checkboxes enabled. KYC audio must never be public.
5. Click **Create bucket**.

---

## 2. Create an IAM user for the app

1. Open **IAM** → **Users** → **Create user**.
2. **User name:** `kyc-transcribe-user`.
3. Create an **access key** for programmatic access.
4. Save the **Access Key ID** and **Secret Access Key** — the secret is shown only once.

---

## 3. Attach a least-privilege policy

Create a policy named `KYCTranscribePolicy` with the JSON below and attach it to the user.
Replace `my-vkyc-audio-bucket` with your bucket name.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-vkyc-audio-bucket",
        "arn:aws:s3:::my-vkyc-audio-bucket/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob"
      ],
      "Resource": "*"
    }
  ]
}
```

**Why this policy:** the app can only read and write one bucket and start or check Transcribe jobs.
If the keys ever leak, they can't access other buckets or AWS services.

---

## 4. Add the keys to `.env`

```env
AWS_ACCESS_KEY_ID=<your access key id>
AWS_SECRET_ACCESS_KEY=<your secret access key>
```

Never commit `.env` — it is already in `.gitignore`.

**Alternative:** install the AWS CLI and run `aws configure`. `boto3` then loads the credentials automatically from `~/.aws/credentials`, and you can leave the keys out of `.env`.

```bash
pip install awscli
aws configure
# AWS Access Key ID, Secret Access Key, region (e.g. ap-south-1), output format: json
```

---

## 5. Test the setup (optional)

**S3 permissions:**

```bash
echo "hello" > test.txt
aws s3 cp test.txt s3://my-vkyc-audio-bucket/test.txt
aws s3 ls s3://my-vkyc-audio-bucket/
```

**Transcribe, end to end:**

```bash
# 1. Convert audio to the best format for Transcribe (mono, 16 kHz WAV)
ffmpeg -i input.mp3 -ac 1 -ar 16000 audio.wav

# 2. Upload to S3
aws s3 cp audio.wav s3://my-vkyc-audio-bucket/audio.wav

# 3. Start a job
aws transcribe start-transcription-job \
  --transcription-job-name kyc-test-job-1 \
  --media MediaFileUri=https://my-vkyc-audio-bucket.s3.ap-south-1.amazonaws.com/audio.wav \
  --media-format wav \
  --language-code en-IN

# 4. Check status: IN_PROGRESS → COMPLETED or FAILED
aws transcribe get-transcription-job --transcription-job-name kyc-test-job-1
```

When the status is `COMPLETED`, the response includes a `TranscriptFileUri` you can download to see the transcript JSON.

> On Windows, if `curl` fails with an SSL error when downloading the transcript, add `--ssl-no-revoke`.

Use only sample audio for testing — never real customer recordings.
