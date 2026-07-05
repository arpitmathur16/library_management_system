class Member:
    def __init__(self, member_id, name, email, phone, join_date):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.join_date = join_date

    def __str__(self):
        return f"[{self.member_id}] {self.name} — {self.email} — Joined: {self.join_date}"