import os
import uuid
from gemini_client import get_image_description, extract_names_from_image
from db import (
    init_db,
    save_analysis,
    search_analysis,
    save_names,
    search_name,
    log_search,
    get_search_counts,
)

def main():
    init_db()
    session_id = str(uuid.uuid4())[:8]

    while True:
        print("\n==== Smart Image Explainer ====")
        print("1. Upload & Analyze Image")
        print("2. Search Previous Results")
        print("3. Exit")
        print("4. Extract Names from Image")
        print("5. Search for Name")
        print("6. View Search Stats")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            filename = input("Enter image filename (from images/ folder): ")
            image_path = os.path.join("images", filename)

            if not os.path.exists(image_path):
                print("Image not found.")
                continue

            print("Analyzing image with Gemini...\n")
            description = get_image_description(image_path)
            print("--- Image Description ---")
            print(description)

        elif choice == "2":
            filename = input("Enter image filename to search: ")
            result = search_analysis(filename)
            if result:
                print("\nResult:\n", result)
            else:
                print("No analysis found.")

        elif choice == "3":
            print("Exiting...")
            break

        elif choice == "4":
            filename = input("Enter image filename (from images/ folder): ")
            image_path = os.path.join("images", filename)
            if not os.path.exists(image_path):
                print("Image not found.")
                continue
            names = extract_names_from_image(image_path)
            print("\nExtracted Names:")
            for name in names:
                print(f"- {name}")

        elif choice == "5":
            name = input("Enter a name to search: ").strip()
            log_search(session_id, name)
            matches = search_name(name)
            if matches:
                print("\nMatches found:")
                for match in matches:
                    print(f"- {match[0]} (from {match[1]} at {match[2]})")
            else:
                print("No match found.")

        elif choice == "6":
            print("\n--- Search Statistics ---")
            for term, count in get_search_counts():
                print(f"{term}: {count} times")

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()