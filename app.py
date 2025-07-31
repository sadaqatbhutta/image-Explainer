import os
from gemini_client import get_image_description
from db import init_db, get_all_analyses, search_by_filename

def main():
    init_db()

    while True:
        print("\n==== Smart Image Explainer ====")
        print("1. Upload & Analyze Image")
        print("2. View All Previous Results")
        print("3. Search by Filename")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            filename = input("Enter image filename (from images/ folder): ")
            image_path = os.path.join("images", filename)

            if not os.path.exists(image_path):
                print("[!] Image not found.")
                continue

            print("Analyzing image with Gemini...\n")
            description = get_image_description(image_path)
            print("\n--- Image Description ---")
            print(description)

        elif choice == "2":
            records = get_all_analyses()
            if not records:
                print("No records found.")
            for rec in records:
                print(f"[{rec[0]}] {rec[1]} - {rec[3]}")
                print(f"   Description: {rec[2]}\n{'-'*50}")

        elif choice == "3":
            query = input("Enter filename or part of it: ").strip()
            results = search_by_filename(query)
            if not results:
                print("No matching records found.")
            for rec in results:
                print(f"[{rec[0]}] {rec[1]} - {rec[3]}")
                print(f"   Description: {rec[2]}\n{'-'*50}")

        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
