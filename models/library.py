from datetime import datetime, timedelta
from database import get_connection
from models.books import Book
from models.member import Member

LOAN_PERIOD_DAYS = 14
LATE_FEE_PER_DAY = 5  # in INR

class Library:

    # ---------- BOOK OPERATIONS ----------
    def add_book(self, title, author, isbn, quantity):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO books (title, author, isbn, quantity, available_quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (title, author, isbn, quantity, quantity))
            conn.commit()
            print(f"✅ Book '{title}' added successfully.")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            conn.close()

    def view_all_books(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No books found.")
            return

        for row in rows:
            book = Book(*row)
            print(book)

    def search_book(self, keyword):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM books WHERE title LIKE ? OR author LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No matching books found.")
            return

        for row in rows:
            print(Book(*row))

    # ---------- MEMBER OPERATIONS ----------
    def register_member(self, name, email, phone):
        conn = get_connection()
        cursor = conn.cursor()
        join_date = datetime.now().strftime("%Y-%m-%d")
        try:
            cursor.execute("""
                INSERT INTO members (name, email, phone, join_date)
                VALUES (?, ?, ?, ?)
            """, (name, email, phone, join_date))
            conn.commit()
            print(f"✅ Member '{name}' registered successfully.")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            conn.close()

    def view_all_members(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No members found.")
            return

        for row in rows:
            print(Member(*row))

    # ---------- TRANSACTION OPERATIONS ----------
    def issue_book(self, book_id, member_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT available_quantity FROM books WHERE book_id = ?", (book_id,))
        result = cursor.fetchone()

        if not result:
            print("❌ Book not found.")
            conn.close()
            return

        if result[0] <= 0:
            print("❌ No available copies to issue.")
            conn.close()
            return

        issue_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=LOAN_PERIOD_DAYS)).strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO transactions (book_id, member_id, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, 'ISSUED')
        """, (book_id, member_id, issue_date, due_date))

        cursor.execute("""
            UPDATE books SET available_quantity = available_quantity - 1 WHERE book_id = ?
        """, (book_id,))

        conn.commit()
        conn.close()
        print(f"✅ Book issued successfully. Due date: {due_date}")

    def return_book(self, txn_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT book_id, due_date, status FROM transactions WHERE txn_id = ?", (txn_id,))
        result = cursor.fetchone()

        if not result:
            print("❌ Transaction not found.")
            conn.close()
            return

        book_id, due_date, status = result

        if status == "RETURNED":
            print("⚠️ This book was already returned.")
            conn.close()
            return

        return_date = datetime.now().strftime("%Y-%m-%d")
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
        return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")

        late_fee = 0
        if return_date_obj > due_date_obj:
            days_late = (return_date_obj - due_date_obj).days
            late_fee = days_late * LATE_FEE_PER_DAY

        cursor.execute("""
            UPDATE transactions SET return_date = ?, status = 'RETURNED' WHERE txn_id = ?
        """, (return_date, txn_id))

        cursor.execute("""
            UPDATE books SET available_quantity = available_quantity + 1 WHERE book_id = ?
        """, (book_id,))

        conn.commit()
        conn.close()

        if late_fee > 0:
            print(f"✅ Book returned. Late fee: ₹{late_fee}")
        else:
            print("✅ Book returned on time. No late fee.")

    def overdue_report(self):
        conn = get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT t.txn_id, b.title, m.name, t.due_date
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            JOIN members m ON t.member_id = m.member_id
            WHERE t.status = 'ISSUED' AND t.due_date < ?
        """, (today,))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("✅ No overdue books.")
            return

        print("\n--- OVERDUE BOOKS ---")
        for txn_id, title, member_name, due_date in rows:
            print(f"Txn #{txn_id} | '{title}' | {member_name} | Due: {due_date}")