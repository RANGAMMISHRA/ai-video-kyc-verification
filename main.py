# main.py
# =============================
# Development helper for testing components
# =============================


from frontend.utils.helper import (
    format_date,
    is_valid_aadhaar,
    is_valid_pan,
    is_valid_mobile,
    capitalize_name
)


def demo():
    print("=== Demo: Utility Functions ===")
    print("Aadhaar valid?", is_valid_aadhaar("123456789012"))
    print("PAN valid?", is_valid_pan("ABCDE1234F"))
    print("Mobile valid?", is_valid_mobile("9876543210"))
    print("Formatted date:", format_date("2025-06-22 14:45:00"))
    print("Capitalized:", capitalize_name("amit sharma"))


def main():
    print("=== Running Main Development Test ===")
    demo()

    # Simulate dummy data for verifier and customer
    dummy_verifier = {
        "organization": "NewAge Bank Ltd",
        "verifier_name": "Raj Mehta",
        "department": "KYC",
        "employee_id": "EMP001",
        "verifier_contact": "9876543210",
        "verifier_email": "raj@newagebank.com"
    }

    dummy_customer = {
        "name": "Amit Sharma",
        "aadhaar": "123456789012",
        "pan": "ABCDE1234F",
        "mobile": "9876543210",
        "email": "amit@gmail.com"
    }

    # Print dummy data
    print("\n=== Dummy Verifier Info ===")
    print(dummy_verifier)

    print("\n=== Dummy Customer Info ===")
    print(dummy_customer)

    # Demonstrate result structure
    dummy_results = {
        "face_match_score": 0.89,
        "blinks": 2,
        "max_angle": 10.2,
        "smile": True,
        "Decision": "Approved ✅"
    }
    print("\n=== Dummy Results ===")
    print(dummy_results)

    print("=== Test Completed Successfully ===")


if __name__ == "__main__":
    main()
