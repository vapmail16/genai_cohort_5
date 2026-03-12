# Class Demo Checklist - IT Support Portal

## ✅ Pre-Class Setup (Do Once)

### 1. Database Setup
```bash
cd /Users/user/Desktop/AI/projects/genai_cohort_5/sdlc_with_llm

# Create database
createdb it_support

# Apply schema
psql -U postgres -d it_support -f database/schema/001_initial.sql
psql -U postgres -d it_support -f database/schema/002_audit_trigger.sql
psql -U postgres -d it_support -f database/schema/003_updated_at_trigger.sql

# Load seed data
psql -U postgres -d it_support -f database/seed.sql

# Verify
python database/test_connection.py
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Create .env
echo "DATABASE_URL=postgresql://postgres:password@localhost/it_support" > .env

# Run tests (should see 23/23 passing)
pytest tests/ -v
```

### 3. Middleware Setup
```bash
cd middleware
npm install

# Create .env
cat > .env << 'EOF'
PORT=3001
JWT_SECRET=dev-secret
BACKEND_URL=http://localhost:8000
NODE_ENV=development
EOF
```

### 4. Frontend Setup
```bash
cd frontend
npm install
```

---

## 🚀 Day of Class (Start Services)

Open 3 terminals:

**Terminal 1 - Backend:**
```bash
cd /Users/user/Desktop/AI/projects/genai_cohort_5/sdlc_with_llm/backend
uvicorn main:app --reload
```

**Terminal 2 - Middleware:**
```bash
cd /Users/user/Desktop/AI/projects/genai_cohort_5/sdlc_with_llm/middleware
npm start
```

**Terminal 3 - Frontend:**
```bash
cd /Users/user/Desktop/AI/projects/genai_cohort_5/sdlc_with_llm/frontend
npm run dev
```

**Open in browser:** http://localhost:5173

---

## 🎓 Live Demo Script (30-40 minutes)

### Part 1: Show Working System (5 min)
- [ ] Login as `john.smith@acmecorp.com`
- [ ] Create a ticket
- [ ] Click on ticket to see detail page
- [ ] Scroll to comments section
- [ ] Point out: "We can VIEW comments but can't ADD new ones!"

### Part 2: BRIDGE Framework (5 min)
- [ ] **B - Business Problem**: "Users need to communicate about tickets"
- [ ] **R - Requirements**: Write user story with students:
  ```
  As an Employee
  I want to add comments to my tickets
  So that I can provide updates to IT support
  ```
- [ ] **I - Test Cases**: Create together:
  1. Valid comment → 201 created
  2. Empty comment → 400 error
  3. Non-existent ticket → 404 error

### Part 3: TDD - Backend (15 min)

**RED Phase (5 min):**
- [ ] Open `backend/tests/test_tickets.py`
- [ ] Add new test:
  ```python
  def test_create_comment_success(test_client, sample_ticket, sample_users):
      response = test_client.post(
          f"/api/tickets/{sample_ticket.id}/comments",
          json={"comment_text": "This is a test comment"}
      )
      assert response.status_code == 201
      data = response.json()
      assert data["comment_text"] == "This is a test comment"
  ```
- [ ] Run: `pytest tests/test_tickets.py::test_create_comment_success -v`
- [ ] Watch it FAIL ❌ (endpoint doesn't exist)

**GREEN Phase (8 min):**
- [ ] Open `backend/routers/tickets.py` line 385
- [ ] Implement minimal endpoint:
  ```python
  @router.post("/{ticket_id}/comments")
  async def create_comment(
      ticket_id: UUID,
      comment_text: str,
      db: AsyncSession = Depends(get_db)
  ):
      # Get ticket
      ticket = await db.get(Ticket, ticket_id)
      if not ticket:
          raise HTTPException(404, "Ticket not found")

      # Create comment
      comment = Comment(
          ticket_id=ticket_id,
          author_id=sample_user_id,  # hardcoded for demo
          comment_text=comment_text
      )
      db.add(comment)
      await db.commit()

      return comment
  ```
- [ ] Run test again: `pytest tests/test_tickets.py::test_create_comment_success -v`
- [ ] Watch it PASS ✅

**REFACTOR Phase (2 min):**
- [ ] Add proper schema validation (CommentCreate, CommentResponse)
- [ ] Add error handling
- [ ] Run all tests: `pytest tests/ -v` (should still pass)

### Part 4: Frontend (10 min)
- [ ] Open `frontend/src/pages/TicketDetail.jsx` line 218
- [ ] Add comment form:
  ```jsx
  {/* Add Comment Form */}
  <div className="mt-6 border-t pt-6">
    <h3 className="font-semibold mb-2">Add Comment</h3>
    <textarea
      value={newComment}
      onChange={(e) => setNewComment(e.target.value)}
      className="w-full border rounded p-2 mb-2"
      rows="3"
      placeholder="Type your comment..."
    />
    <button
      onClick={handleAddComment}
      className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
    >
      Add Comment
    </button>
  </div>
  ```
- [ ] Add handler:
  ```jsx
  const handleAddComment = async () => {
    await apiClient.post(`/api/tickets/${id}/comments`, {
      comment_text: newComment
    });
    setNewComment('');
    // Reload ticket to show new comment
    fetchTicket();
  };
  ```

### Part 5: Test End-to-End (5 min)
- [ ] Refresh browser
- [ ] Go to a ticket
- [ ] Type a comment: "This feature was built live using TDD!"
- [ ] Click "Add Comment"
- [ ] See comment appear immediately
- [ ] Check database: `psql -d it_support -c "SELECT * FROM ticket_comments ORDER BY created_at DESC LIMIT 1;"`

---

## 📚 Key Teaching Points

### TDD Methodology
- ✅ **Test First** - Write failing test before code
- ✅ **RED** - Watch it fail (proves test works)
- ✅ **GREEN** - Write minimal code to pass
- ✅ **REFACTOR** - Improve code quality

### BRIDGE Framework
- ✅ **B** - Business Problem (clear need)
- ✅ **R** - Requirements (user story)
- ✅ **I** - Iterative Testing (test cases)
- ✅ **D** - Data (sample comment)
- ✅ **G** - Guided Execution (implement with TDD)
- ✅ **E** - Evaluate (tests pass, feature works)

### Full-Stack Integration
- ✅ Database table already exists
- ✅ Backend API endpoint
- ✅ Frontend UI form
- ✅ Everything works together

---

## 🎯 What Students Will Learn

1. **TDD is practical** - Not just theory, works in real projects
2. **Tests give confidence** - Can refactor without fear
3. **BRIDGE is systematic** - Clear steps from problem to solution
4. **Full-stack development** - How all layers connect
5. **Small iterations work** - Build feature in 30 minutes

---

## 📊 Project Stats to Share

- **Total files:** 50+ source files
- **Backend tests:** 23/23 passing (100%)
- **Lines of code:** ~3,000+
- **Time to build:** ~6 hours (automated with AI)
- **Time to add feature:** ~30 minutes (with TDD)

---

## 🔧 Troubleshooting

**Backend won't start:**
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r backend/requirements.txt
```

**Database errors:**
```bash
# Reset database
dropdb it_support
createdb it_support
# Re-run all schema files
```

**Frontend can't connect:**
- Check middleware is running on port 3001
- Check browser console for errors
- Verify CORS settings in backend

---

## ✅ Success Criteria

After the demo, students should be able to:
- [ ] Explain RED-GREEN-REFACTOR cycle
- [ ] Write a simple backend test
- [ ] Understand the value of TDD
- [ ] See how BRIDGE framework guides development
- [ ] Appreciate full-stack integration

---

**You're ready! Good luck with your class! 🚀**
