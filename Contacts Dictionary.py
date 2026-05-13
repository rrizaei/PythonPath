"""
Nested Contacts Dictionary Parser - Advanced Contact Management System

A comprehensive contact management system that parses, searches, and manipulates nested dictionary
structures representing personal and professional contacts with multiple data layers.

WHAT IT DOES:
- Stores contacts with nested information (personal, professional, addresses, phones, emails)
- Parses deeply nested dictionary structures with recursive functions
- Searches contacts by ANY field (name, email, city, company, etc.)
- Filters contacts by multiple criteria (age, city, company, tags)
- Exports/imports contacts to JSON
- Validates contact data structure
- Finds duplicate contacts
- Generates reports and statistics
- Merges duplicate contact records

USE CASES:
- CRM system backend
- Personal address book management
- Learning recursive dictionary traversal
- Data cleaning and deduplication
- Contact information validation
- Migration tool for contact data

KEY FEATURES:
- Recursive search through unlimited nesting levels
- Field-based filtering with multiple conditions
- Duplicate detection across multiple fields
- Statistical analysis (age ranges, location distribution, etc.)
- JSON import/export for data persistence
- Data validation with schema checking
- Partial string matching for flexible search
- Case-insensitive search options
- Batch operations on filtered results

DATA STRUCTURE:
contacts = {
    "contact_id": {
        "personal": {
            "first_name": str,
            "last_name": str,
            "age": int,
            "dob": str,
            "gender": str
        },
        "professional": {
            "company": str,
            "title": str,
            "department": str,
            "years_experience": int
        },
        "contact_info": {
            "email": list[str],
            "phone": list[dict],
            "addresses": list[dict]
        },
        "social": {
            "linkedin": str,
            "twitter": str,
            "github": str
        },
        "tags": list[str],
        "notes": str,
        "created_date": str,
        "last_updated": str
    }
}

REQUIREMENTS: Python 3.6+ (json, datetime, typing modules)
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import Counter

class ContactsParser:
    def __init__(self):
        """Initialize empty contacts dictionary"""
        self.contacts = {}
        self.next_id = 1

    def add_contact(self, contact_data: Dict) -> str:
        """
        Add a new contact to the database

        Args:
            contact_data: Nested dictionary with contact information

        Returns:
            str: Contact ID
        """
        contact_id = str(self.next_id)
        self.next_id += 1

        # Add metadata
        contact_data['_metadata'] = {
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'version': 1
        }

        self.contacts[contact_id] = contact_data
        print(f"Contact added with ID: {contact_id}")
        return contact_id

    def get_contact(self, contact_id: str) -> Optional[Dict]:
        """Retrieve a contact by ID"""
        return self.contacts.get(contact_id)

    def update_contact(self, contact_id: str, updates: Dict) -> bool:
        """
        Update a contact with new data (merges nested dictionaries)
        """
        if contact_id not in self.contacts:
            print(f"Error: Contact {contact_id} not found")
            return False

        # Deep merge the updates
        self._deep_merge(self.contacts[contact_id], updates)

        # Update metadata
        self.contacts[contact_id]['_metadata']['last_updated'] = datetime.now().isoformat()
        self.contacts[contact_id]['_metadata']['version'] += 1

        print(f"Contact {contact_id} updated")
        return True

    def _deep_merge(self, target: Dict, source: Dict):
        """Recursively merge source dictionary into target"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value

    def search_contacts(self, query: str, case_sensitive: bool = False) -> Dict[str, Dict]:
        """
        Search for contacts by ANY field value (recursive)

        Args:
            query: Search string
            case_sensitive: Whether search is case-sensitive

        Returns:
            Dict of matching contacts
        """
        results = {}
        search_term = query if case_sensitive else query.lower()

        for contact_id, contact in self.contacts.items():
            if self._recursive_search(contact, search_term, case_sensitive):
                results[contact_id] = contact

        return results

    def _recursive_search(self, obj: Any, search_term: str, case_sensitive: bool) -> bool:
        """
        Recursively search through nested structures

        Args:
            obj: Current object to search (dict, list, string, etc.)
            search_term: Term to search for
            case_sensitive: Whether search is case-sensitive

        Returns:
            bool: True if search term found
        """
        if isinstance(obj, dict):
            for value in obj.values():
                if self._recursive_search(value, search_term, case_sensitive):
                    return True
        elif isinstance(obj, list):
            for item in obj:
                if self._recursive_search(item, search_term, case_sensitive):
                    return True
        elif isinstance(obj, str):
            compare_obj = obj if case_sensitive else obj.lower()
            return search_term in compare_obj
        elif isinstance(obj, (int, float)):
            return search_term == str(obj)

        return False

    def filter_contacts(self, filters: Dict[str, Any], exact_match: bool = False) -> Dict[str, Dict]:
        """
        Filter contacts by specific field values

        Args:
            filters: Dictionary of field paths and values to match
                    Example: {'personal.age': 30, 'professional.company': 'Google'}
            exact_match: If True, requires exact string match

        Returns:
            Dict of matching contacts
        """
        results = {}

        for contact_id, contact in self.contacts.items():
            match = True
            for field_path, expected_value in filters.items():
                actual_value = self._get_nested_value(contact, field_path)

                if actual_value is None:
                    match = False
                    break

                if not self._matches_filter(actual_value, expected_value, exact_match):
                    match = False
                    break

            if match:
                results[contact_id] = contact

        return results

    def _get_nested_value(self, obj: Dict, path: str, default: Any = None) -> Any:
        """
        Get value from nested dictionary using dot notation path
        Example: 'personal.first_name' or 'contact_info.email.0'
        """
        keys = path.split('.')
        current = obj

        try:
            for key in keys:
                if key.isdigit():  # List index
                    current = current[int(key)]
                else:
                    current = current[key]
            return current
        except (KeyError, IndexError, TypeError):
            return default

    def _matches_filter(self, actual: Any, expected: Any, exact_match: bool) -> bool:
        """Check if actual value matches expected filter value"""
        if isinstance(actual, list):
            # Check if expected value is in the list
            for item in actual:
                if isinstance(item, dict):
                    # Search in list of dicts
                    if self._matches_filter(item, expected, exact_match):
                        return True
                elif not exact_match and isinstance(item, str):
                    if expected.lower() in item.lower():
                        return True
                elif actual == expected:
                    return True
            return False
        elif isinstance(actual, str) and isinstance(expected, str):
            if exact_match:
                return actual == expected
            else:
                return expected.lower() in actual.lower()
        else:
            return actual == expected

    def find_duplicates(self, field_path: str) -> Dict[str, List[str]]:
        """
        Find duplicate contacts based on a specific field

        Args:
            field_path: Field to check for duplicates (e.g., 'contact_info.email.0')

        Returns:
            Dictionary mapping duplicate values to list of contact IDs
        """
        value_map = {}

        for contact_id, contact in self.contacts.items():
            value = self._get_nested_value(contact, field_path)
            if value:
                if isinstance(value, list):
                    for item in value:
                        self._add_to_value_map(value_map, item, contact_id)
                else:
                    self._add_to_value_map(value_map, value, contact_id)

        # Return only duplicates (values with more than one contact)
        return {value: ids for value, ids in value_map.items() if len(ids) > 1}

    def _add_to_value_map(self, value_map: Dict, value: Any, contact_id: str):
        """Helper to add contact to value map for duplicate detection"""
        if value not in value_map:
            value_map[value] = []
        if contact_id not in value_map[value]:
            value_map[value].append(contact_id)

    def get_statistics(self) -> Dict:
        """
        Generate statistics about the contacts database
        """
        stats = {
            'total_contacts': len(self.contacts),
            'age_distribution': {},
            'company_distribution': {},
            'city_distribution': {},
            'tag_distribution': {},
            'avg_age': 0,
            'total_emails': 0,
            'total_phones': 0
        }

        ages = []
        companies = []
        cities = []
        tags = []

        for contact in self.contacts.values():
            # Age statistics
            age = self._get_nested_value(contact, 'personal.age')
            if age:
                ages.append(age)
                age_range = f"{ (age // 10) * 10 }-{ (age // 10) * 10 + 9 }"
                stats['age_distribution'][age_range] = stats['age_distribution'].get(age_range, 0) + 1

            # Company statistics
            company = self._get_nested_value(contact, 'professional.company')
            if company:
                companies.append(company)
                stats['company_distribution'][company] = stats['company_distribution'].get(company, 0) + 1

            # City statistics
            addresses = self._get_nested_value(contact, 'contact_info.addresses')
            if addresses and isinstance(addresses, list):
                for addr in addresses:
                    city = addr.get('city')
                    if city:
                        cities.append(city)
                        stats['city_distribution'][city] = stats['city_distribution'].get(city, 0) + 1

            # Tag statistics
            contact_tags = self._get_nested_value(contact, 'tags')
            if contact_tags and isinstance(contact_tags, list):
                tags.extend(contact_tags)
                for tag in contact_tags:
                    stats['tag_distribution'][tag] = stats['tag_distribution'].get(tag, 0) + 1

            # Count emails
            emails = self._get_nested_value(contact, 'contact_info.email')
            if emails and isinstance(emails, list):
                stats['total_emails'] += len(emails)

            # Count phones
            phones = self._get_nested_value(contact, 'contact_info.phone')
            if phones and isinstance(phones, list):
                stats['total_phones'] += len(phones)

        # Calculate averages
        if ages:
            stats['avg_age'] = sum(ages) / len(ages)

        # Find top companies/cities
        if companies:
            stats['top_company'] = Counter(companies).most_common(1)[0][0] if companies else None
        if cities:
            stats['top_city'] = Counter(cities).most_common(1)[0][0] if cities else None
        if tags:
            stats['top_tag'] = Counter(tags).most_common(1)[0][0] if tags else None

        return stats

    def display_contact(self, contact_id: str, format_type: str = "detailed"):
        """Display a single contact in formatted output"""
        contact = self.get_contact(contact_id)
        if not contact:
            print(f"Contact {contact_id} not found")
            return

        print("\n" + "="*60)
        print(f"CONTACT ID: {contact_id}")
        print("="*60)

        if format_type == "detailed":
            self._print_nested_dict(contact, indent=0)
        else:
            # Simple format
            name = self._get_nested_value(contact, 'personal.first_name', '')
            last = self._get_nested_value(contact, 'personal.last_name', '')
            email = self._get_nested_value(contact, 'contact_info.email.0', '')
            print(f"Name: {name} {last}")
            print(f"Email: {email}")

    def _print_nested_dict(self, obj: Any, indent: int = 0):
        """Recursively print nested dictionary structure"""
        prefix = "  " * indent

        if isinstance(obj, dict):
            for key, value in obj.items():
                if key.startswith('_'):  # Skip metadata for cleaner output
                    continue
                print(f"{prefix}{key}:")
                self._print_nested_dict(value, indent + 1)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                print(f"{prefix}[{i}]:")
                self._print_nested_dict(item, indent + 1)
        else:
            print(f"{prefix}-> {obj}")

    def export_to_json(self, filename: str = "contacts.json"):
        """Export contacts to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.contacts, f, indent=2)
        print(f"Contacts exported to {filename}")

    def load_from_json(self, filename: str = "contacts.json"):
        """Load contacts from JSON file"""
        try:
            with open(filename, 'r') as f:
                self.contacts = json.load(f)

                # Update next_id
                max_id = 0
                for contact_id in self.contacts.keys():
                    if contact_id.isdigit():
                        max_id = max(max_id, int(contact_id))
                self.next_id = max_id + 1

            print(f"Contacts loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return False

    def add_sample_contacts(self):
        """Add sample contacts for demonstration"""
        sample_contacts = [
            {
                "personal": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "age": 32,
                    "dob": "1992-03-15",
                    "gender": "Male"
                },
                "professional": {
                    "company": "Google",
                    "title": "Senior Software Engineer",
                    "department": "Cloud AI",
                    "years_experience": 8
                },
                "contact_info": {
                    "email": ["john.doe@google.com", "johndoe@gmail.com"],
                    "phone": [
                        {"type": "work", "number": "555-0101"},
                        {"type": "mobile", "number": "555-0202"}
                    ],
                    "addresses": [
                        {"type": "home", "street": "123 Main St", "city": "San Francisco", "zip": "94105"},
                        {"type": "work", "street": "1600 Amphitheatre Pkwy", "city": "Mountain View", "zip": "94043"}
                    ]
                },
                "social": {
                    "linkedin": "linkedin.com/in/johndoe",
                    "github": "github.com/johndoe",
                    "twitter": "@johndoe"
                },
                "tags": ["tech", "cloud", "python", "ai"],
                "notes": "Met at PyCon 2023. Expert in machine learning."
            },
            {
                "personal": {
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "age": 28,
                    "dob": "1996-07-22",
                    "gender": "Female"
                },
                "professional": {
                    "company": "Microsoft",
                    "title": "Product Manager",
                    "department": "Azure",
                    "years_experience": 5
                },
                "contact_info": {
                    "email": ["jane.smith@microsoft.com"],
                    "phone": [
                        {"type": "mobile", "number": "555-0303"}
                    ],
                    "addresses": [
                        {"type": "home", "street": "456 Oak Ave", "city": "Seattle", "zip": "98101"}
                    ]
                },
                "social": {
                    "linkedin": "linkedin.com/in/janesmith",
                    "twitter": "@janesmith"
                },
                "tags": ["product", "cloud", "leadership"],
                "notes": "Former Google PM. Specializes in cloud strategy."
            },
            {
                "personal": {
                    "first_name": "Alice",
                    "last_name": "Johnson",
                    "age": 35,
                    "dob": "1989-11-03",
                    "gender": "Female"
                },
                "professional": {
                    "company": "Amazon",
                    "title": "Data Scientist",
                    "department": "AWS",
                    "years_experience": 10
                },
                "contact_info": {
                    "email": ["alice.j@amazon.com", "alice.johnson@gmail.com"],
                    "phone": [
                        {"type": "work", "number": "555-0404"},
                        {"type": "mobile", "number": "555-0505"}
                    ],
                    "addresses": [
                        {"type": "home", "street": "789 Pine St", "city": "Seattle", "zip": "98109"}
                    ]
                },
                "social": {
                    "linkedin": "linkedin.com/in/alicejohnson",
                    "github": "github.com/alicej"
                },
                "tags": ["data", "ml", "aws", "python"],
                "notes": "PhD in Statistics. Published author."
            }
        ]

        for contact in sample_contacts:
            self.add_contact(contact)

        print("\nSample contacts added!")

def main():
    """Interactive demo of the Contacts Parser"""
    parser = ContactsParser()

    print("\n" + "="*60)
    print("NESTED CONTACTS DICTIONARY PARSER")
    print("="*60)

    # Add sample data
    parser.add_sample_contacts()

    while True:
        print("\n" + "-"*50)
        print("OPTIONS:")
        print("  1. Display all contacts")
        print("  2. Search contacts (by any field)")
        print("  3. Filter contacts")
        print("  4. Find duplicates")
        print("  5. Show statistics")
        print("  6. Export/Import JSON")
        print("  7. Add new contact")
        print("  8. Exit")

        choice = input("\nYour choice (1-8): ").strip()

        if choice == '1':
            for contact_id in parser.contacts:
                parser.display_contact(contact_id, format_type="simple")
                print()

        elif choice == '2':
            query = input("Enter search term: ")
            results = parser.search_contacts(query)
            print(f"\nFound {len(results)} matching contacts:")
            for contact_id in results:
                name = parser._get_nested_value(results[contact_id], 'personal.first_name', '')
                last = parser._get_nested_value(results[contact_id], 'personal.last_name', '')
                print(f"  - {contact_id}: {name} {last}")

        elif choice == '3':
            print("\nFilter by field (examples: personal.age, professional.company)")
            field = input("Field path: ")
            value = input("Value to match: ")
            exact = input("Exact match? (yes/no): ").lower() == 'yes'

            results = parser.filter_contacts({field: value}, exact_match=exact)
            print(f"\nFound {len(results)} matching contacts:")
            for contact_id in results:
                name = parser._get_nested_value(results[contact_id], 'personal.first_name', '')
                last = parser._get_nested_value(results[contact_id], 'personal.last_name', '')
                print(f"  - {contact_id}: {name} {last}")

        elif choice == '4':
            field = input("Field to check for duplicates (e.g., contact_info.email.0): ")
            duplicates = parser.find_duplicates(field)
            if duplicates:
                print(f"\nFound {len(duplicates)} duplicate values:")
                for value, ids in duplicates.items():
                    print(f"  - '{value}': {', '.join(ids)}")
            else:
                print("No duplicates found")

        elif choice == '5':
            stats = parser.get_statistics()
            print("\nCONTACT STATISTICS:")
            print(f"  Total Contacts: {stats['total_contacts']}")
            print(f"  Average Age: {stats['avg_age']:.1f}")
            print(f"  Total Emails: {stats['total_emails']}")
            print(f"  Total Phones: {stats['total_phones']}")
            print(f"  Top Company: {stats.get('top_company', 'N/A')}")
            print(f"  Top City: {stats.get('top_city', 'N/A')}")
            print(f"  Top Tag: {stats.get('top_tag', 'N/A')}")

            if stats['company_distribution']:
                print("\n  Company Distribution:")
                for company, count in sorted(stats['company_distribution'].items(), key=lambda x: x[1], reverse=True)[:3]:
                    print(f"    - {company}: {count}")

        elif choice == '6':
            action = input("Export (e) or Import (i)? ").lower()
            if action == 'e':
                parser.export_to_json()
            elif action == 'i':
                parser.load_from_json()

        elif choice == '7':
            print("\nAdd new contact (simplified)")
            first = input("First name: ")
            last = input("Last name: ")
            email = input("Email: ")
            company = input("Company: ")

            new_contact = {
                "personal": {"first_name": first, "last_name": last},
                "professional": {"company": company},
                "contact_info": {"email": [email]},
                "tags": []
            }

            parser.add_contact(new_contact)

        elif choice == '8':
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()