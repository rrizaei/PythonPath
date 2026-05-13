"""
Movie Schedule Dictionary - Cinema Showtime Manager

A comprehensive movie schedule management system that stores, displays, and manages movie showtimes
across multiple theaters/days. Perfect for small cinemas, home theaters, or learning dictionary data structures.

WHAT IT DOES:
- Stores movies with showtimes, theaters, and prices
- Adds/removes movies from schedule
- Searches for movies by title, time, or theater
- Displays schedule in various formats (by day, by theater, by time)
- Calculates total revenue potential
- Finds available time slots
- Shows what's playing now/next

USE CASES:
- Small cinema or independent theater management
- Home movie marathon planning
- Learning nested dictionary structures in Python
- Event scheduling system prototype
- Movie theater lobby display system

KEY FEATURES:
- Nested dictionary architecture (days → theaters → movies → showtimes)
- Multiple search and filter options
- Conflict detection (no overlapping showtimes in same theater)
- Revenue calculation
- Formatted schedule display
- Easy data export to JSON
- Time-based queries (now playing, upcoming shows)

DATA STRUCTURE:
schedule = {
    "Monday": {
        "Theater 1": [
            {"title": "Movie Name", "time": "14:00", "price": 12.50, "duration": 120},
            ...
        ]
    }
}

REQUIREMENTS: Python 3.6+ (datetime module for time operations, json for export)
"""

from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Tuple

class MovieSchedule:
    def __init__(self):
        """Initialize empty movie schedule"""
        self.schedule = {}
        self.theaters = ["Theater 1", "Theater 2", "Theater 3", "Theater 4"]
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Initialize schedule with empty theaters for each day
        for day in self.days:
            self.schedule[day] = {}
            for theater in self.theaters:
                self.schedule[day][theater] = []

    def add_movie(self, day: str, theater: str, title: str, time: str,
                  price: float, duration: int, rating: str = "NR") -> bool:
        """
        Add a movie to the schedule

        Args:
            day: Day of week (Monday-Sunday)
            theater: Theater number/name
            title: Movie title
            time: Showtime (HH:MM format)
            price: Ticket price
            duration: Movie length in minutes
            rating: Movie rating (G, PG, PG-13, R, NR)

        Returns:
            bool: True if added successfully, False if time conflict
        """
        # Validate inputs
        if day not in self.schedule:
            print(f"Error: Invalid day '{day}'. Use: {', '.join(self.days)}")
            return False

        if theater not in self.schedule[day]:
            print(f"Error: Invalid theater '{theater}'. Use: {', '.join(self.theaters)}")
            return False

        # Check for time conflicts
        for movie in self.schedule[day][theater]:
            if self._time_overlap(movie['time'], movie['duration'], time, duration):
                print(f"Error: Time conflict with '{movie['title']}' at {movie['time']}")
                return False

        # Add the movie
        movie_entry = {
            'title': title,
            'time': time,
            'price': price,
            'duration': duration,
            'rating': rating,
            'end_time': self._calculate_end_time(time, duration)
        }

        # Insert in chronological order
        self.schedule[day][theater].append(movie_entry)
        self.schedule[day][theater].sort(key=lambda x: x['time'])

        print(f"✓ Added '{title}' to {day} at {theater} - {time}")
        return True

    def _time_overlap(self, time1: str, duration1: int, time2: str, duration2: int) -> bool:
        """Check if two showtimes overlap"""
        start1 = datetime.strptime(time1, "%H:%M")
        end1 = start1 + timedelta(minutes=duration1)
        start2 = datetime.strptime(time2, "%H:%M")
        end2 = start2 + timedelta(minutes=duration2)

        return max(start1, start2) < min(end1, end2)

    def _calculate_end_time(self, start_time: str, duration: int) -> str:
        """Calculate end time based on start time and duration"""
        start = datetime.strptime(start_time, "%H:%M")
        end = start + timedelta(minutes=duration)
        return end.strftime("%H:%M")

    def remove_movie(self, day: str, theater: str, title: str, time: str = None) -> bool:
        """Remove a movie from the schedule"""
        if day not in self.schedule or theater not in self.schedule[day]:
            return False

        for i, movie in enumerate(self.schedule[day][theater]):
            if movie['title'].lower() == title.lower():
                if time is None or movie['time'] == time:
                    removed = self.schedule[day][theater].pop(i)
                    print(f"✓ Removed '{removed['title']}' from {day} at {theater}")
                    return True

        print(f"Error: Movie '{title}' not found")
        return False

    def search_movie(self, title: str) -> List[Dict]:
        """Search for a movie across all schedules"""
        results = []
        for day in self.days:
            for theater in self.theaters:
                for movie in self.schedule[day][theater]:
                    if title.lower() in movie['title'].lower():
                        results.append({
                            'day': day,
                            'theater': theater,
                            **movie
                        })
        return results

    def search_by_time(self, search_time: str, day: str = None) -> List[Dict]:
        """Find movies showing at or near a specific time"""
        results = []
        days_to_check = [day] if day else self.days

        for current_day in days_to_check:
            for theater in self.theaters:
                for movie in self.schedule[current_day][theater]:
                    if movie['time'] <= search_time <= movie['end_time']:
                        results.append({
                            'day': current_day,
                            'theater': theater,
                            **movie
                        })
        return results

    def what_is_playing_now(self, day: str = None) -> List[Dict]:
        """Find movies currently playing (based on current system time)"""
        now = datetime.now().strftime("%H:%M")
        return self.search_by_time(now, day)

    def get_daily_schedule(self, day: str) -> Dict:
        """Get complete schedule for a specific day"""
        if day not in self.schedule:
            print(f"Error: Invalid day '{day}'")
            return {}
        return self.schedule[day]

    def display_schedule(self, day: str = None, format_type: str = "table"):
        """
        Display schedule in various formats

        format_type: "table", "simple", "detailed", "theater_view"
        """
        days_to_show = [day] if day else self.days

        print("\n" + "="*80)
        print("MOVIE SCHEDULE")
        print("="*80)

        for current_day in days_to_show:
            if current_day not in self.schedule:
                continue

            print(f"\n📅 {current_day.upper()}")
            print("-"*80)

            has_movies = False
            for theater in self.theaters:
                movies = self.schedule[current_day][theater]
                if movies:
                    has_movies = True
                    print(f"\n🎬 {theater}:")

                    for movie in movies:
                        if format_type == "detailed":
                            print(f"   • {movie['time']} - {movie['title']} "
                                  f"({movie['duration']} min) "
                                  f"[{movie['rating']}] - ${movie['price']:.2f}")
                            print(f"     Ends at: {movie['end_time']}")
                        else:
                            print(f"   • {movie['time']} - {movie['title']} "
                                  f"({movie['duration']} min) - ${movie['price']:.2f}")

            if not has_movies:
                print("   No movies scheduled")

    def get_revenue_potential(self, day: str = None) -> Dict:
        """Calculate total potential revenue from scheduled movies"""
        revenue = {}
        days_to_calc = [day] if day else self.days

        total_revenue = 0
        total_movies = 0

        for current_day in days_to_calc:
            day_revenue = 0
            day_movies = 0

            for theater in self.theaters:
                for movie in self.schedule[current_day][theater]:
                    day_revenue += movie['price']
                    day_movies += 1

            revenue[current_day] = {'revenue': day_revenue, 'movies': day_movies}
            total_revenue += day_revenue
            total_movies += day_movies

        revenue['total'] = {'revenue': total_revenue, 'movies': total_movies}
        return revenue

    def export_to_json(self, filename: str = "movie_schedule.json"):
        """Export schedule to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.schedule, f, indent=2)
        print(f"✓ Schedule exported to {filename}")

    def load_from_json(self, filename: str = "movie_schedule.json"):
        """Load schedule from JSON file"""
        try:
            with open(filename, 'r') as f:
                self.schedule = json.load(f)
            print(f"✓ Schedule loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return False

    def find_available_slots(self, day: str, theater: str, duration: int) -> List[str]:
        """Find available time slots for a new movie"""
        if theater not in self.schedule[day]:
            return []

        occupied_slots = []
        for movie in self.schedule[day][theater]:
            occupied_slots.append((movie['time'], movie['end_time']))

        # Available time slots (9 AM to 11 PM)
        available = []
        current_time = datetime.strptime("09:00", "%H:%M")
        end_of_day = datetime.strptime("23:00", "%H:%M")

        while current_time <= end_of_day:
            current_time_str = current_time.strftime("%H:%M")
            possible_end = current_time + timedelta(minutes=duration)

            if possible_end > end_of_day:
                break

            # Check if slot conflicts with any movie
            conflict = False
            for start, end in occupied_slots:
                slot_start = datetime.strptime(start, "%H:%M")
                slot_end = datetime.strptime(end, "%H:%M")
                if max(current_time, slot_start) < min(possible_end, slot_end):
                    conflict = True
                    break

            if not conflict:
                available.append(current_time_str)

            current_time += timedelta(minutes=30)  # 30-minute increments

        return available

    def add_sample_data(self):
        """Add sample movies for demonstration"""
        sample_movies = [
            ("Monday", "Theater 1", "Inception", "14:00", 12.50, 148, "PG-13"),
            ("Monday", "Theater 1", "The Dark Knight", "19:00", 14.00, 152, "PG-13"),
            ("Monday", "Theater 2", "Barbie", "15:30", 13.00, 114, "PG-13"),
            ("Tuesday", "Theater 1", "Oppenheimer", "16:00", 15.00, 180, "R"),
            ("Wednesday", "Theater 3", "Interstellar", "18:00", 13.50, 169, "PG-13"),
            ("Friday", "Theater 1", "Dune: Part Two", "20:00", 16.00, 166, "PG-13"),
            ("Saturday", "Theater 1", "Wonka", "13:00", 11.00, 116, "PG"),
            ("Saturday", "Theater 2", "Poor Things", "19:30", 14.00, 141, "R"),
            ("Sunday", "Theater 4", "The Boy and the Heron", "15:00", 12.00, 124, "PG-13"),
        ]

        for movie in sample_movies:
            self.add_movie(*movie)

        print("\n✓ Sample movies added to schedule!")

def main():
    """Interactive demo of the Movie Schedule system"""
    schedule = MovieSchedule()

    print("\n" + "="*80)
    print("MOVIE SCHEDULE MANAGER")
    print("="*80)

    # Add sample data
    schedule.add_sample_data()

    while True:
        print("\n" + "-"*50)
        print("OPTIONS:")
        print("  1. Display full schedule")
        print("  2. Search for a movie")
        print("  3. What's playing now?")
        print("  4. Show revenue potential")
        print("  5. Find available time slots")
        print("  6. Add a movie")
        print("  7. Remove a movie")
        print("  8. Export to JSON")
        print("  9. Exit")

        choice = input("\nYour choice (1-9): ").strip()

        if choice == '1':
            schedule.display_schedule(format_type="detailed")

        elif choice == '2':
            title = input("Enter movie title to search: ")
            results = schedule.search_movie(title)
            if results:
                print(f"\nFound {len(results)} showings:")
                for r in results:
                    print(f"  • {r['day']} at {r['theater']} - {r['time']} "
                          f"({r['duration']} min) - ${r['price']:.2f}")
            else:
                print(f"No showings found for '{title}'")

        elif choice == '3':
            now_playing = schedule.what_is_playing_now()
            if now_playing:
                print("\n🎬 NOW PLAYING:")
                for movie in now_playing:
                    print(f"  • {movie['title']} at {movie['theater']} "
                          f"({movie['day']} - {movie['time']})")
            else:
                print("No movies currently playing")

        elif choice == '4':
            revenue = schedule.get_revenue_potential()
            print("\n💰 REVENUE POTENTIAL:")
            for day, data in revenue.items():
                if day != 'total':
                    print(f"  {day}: ${data['revenue']:.2f} ({data['movies']} movies)")
            print(f"  TOTAL: ${revenue['total']['revenue']:.2f} "
                  f"({revenue['total']['movies']} movies total)")

        elif choice == '5':
            day = input("Enter day: ").capitalize()
            theater = input("Enter theater (Theater 1-4): ")
            try:
                duration = int(input("Enter movie duration (minutes): "))
                slots = schedule.find_available_slots(day, theater, duration)
                if slots:
                    print(f"\nAvailable time slots on {day} at {theater}:")
                    for slot in slots[:10]:  # Show first 10
                        print(f"  • {slot}")
                else:
                    print("No available slots found")
            except ValueError:
                print("Invalid duration")

        elif choice == '6':
            day = input("Day: ").capitalize()
            theater = input("Theater: ")
            title = input("Movie title: ")
            time = input("Showtime (HH:MM): ")
            try:
                price = float(input("Ticket price: $"))
                duration = int(input("Duration (minutes): "))
                rating = input("Rating (G/PG/PG-13/R/NR): ").upper()
                schedule.add_movie(day, theater, title, time, price, duration, rating)
            except ValueError:
                print("Invalid price or duration")

        elif choice == '7':
            day = input("Day: ").capitalize()
            theater = input("Theater: ")
            title = input("Movie title: ")
            time = input("Showtime (HH:MM) [optional]: ") or None
            schedule.remove_movie(day, theater, title, time)

        elif choice == '8':
            schedule.export_to_json()

        elif choice == '9':
            print("\nGoodbye! 🎬")
            break

        else:
            print("Invalid choice. Please enter 1-9")

if __name__ == "__main__":
    main()