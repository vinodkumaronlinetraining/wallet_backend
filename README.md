## React Sessions — Complete Summary

---

## What is React and Why Use It

React is a **JavaScript library** for building UIs using reusable components.

```
Traditional HTML/JS approach problems:
- Manual DOM updates → document.getElementById("balance").textContent = ...
- Page reloads on navigation
- Duplicate HTML across files (nav copied in every page)
- No shared state — localStorage used as workaround

React solves all of these:
- Automatic UI updates when data changes
- Single page application (SPA) — no reloads
- Components written once, used everywhere
- Global state via Context API
```

---

## Topic 1 — Setup and Project Structure

```bash
# create project
npm create vite@latest wallet-app
cd wallet-app
npm install
npm install react-router-dom
npm run dev
```

### Key files explained

```
index.html    → single HTML file with <div id="root"> — React mounts here
main.jsx      → entry point — renders App into #root
App.jsx       → main component — defines app structure
```

```jsx
// main.jsx — entry point
createRoot(document.getElementById('root')).render(
    <StrictMode>
        <App />
    </StrictMode>
)
```

### Final folder structure for wallet app

```
src/
    components/
        Navbar.jsx
        StatCard.jsx
        TransactionForm.jsx
    pages/
        Dashboard.jsx
        Login.jsx
        Register.jsx
        Transactions.jsx
        Profile.jsx
    services/
        api.jsx
    UserContext.jsx
    App.jsx
    main.jsx
public/
    wallet.css
```

---

## Topic 2 — Components and JSX

Components are **functions that return JSX** — reusable pieces of UI.

```jsx
// rules:
// 1. component name must start with capital letter
// 2. must return ONE parent element
// 3. use className instead of class
// 4. JS expressions go inside {}
// 5. self closing tags need /> e.g. <img />
// 6. comments use {/* */}

function Navbar() {
    return (
        <header>
            <nav>
                <a href="/" className="nav-logo">₹ Wallet App</a>
                <div className="nav-links">
                    <a href="/dashboard">Dashboard</a>
                    <a href="/transactions">Transactions</a>
                    <a href="/profile">Profile</a>
                </div>
            </nav>
        </header>
    );
}
export default Navbar;
```

### JSX differences from HTML

```jsx
// HTML              →   JSX
class="stat-card"   →   className="stat-card"
for="amount"        →   htmlFor="amount"
onclick="..."       →   onClick={...}
<!-- comment -->    →   {/* comment */}
<img>               →   <img />
```

### JS expressions in JSX

```jsx
function App() {
    const user = { name: "Vinod", balance: 1445.50 };
    return (
        <div>
            <h1>Welcome back, {user.name}!</h1>
            <p>Balance: ₹ {user.balance.toFixed(2)}</p>
            {/* conditional rendering */}
            {user.balance > 1000
                ? <span>Balance is good</span>
                : <span>Balance is low</span>
            }
        </div>
    );
}
```

---

## Topic 3 — Props

Props pass data from **parent → child** component. Makes components reusable.

```jsx
// StatCard — reusable with props
function StatCard({ title, value, color }) {
    return (
        <div className={`stat-card ${color}`}>
            <div className="stat-label">{title}</div>
            <div className="stat-value">{value}</div>
        </div>
    );
}

// used 4 times with different data — replaces 4 hardcoded HTML divs
<div className="stats-row">
    <StatCard title="Wallet Balance" value={`₹ ${balance.toFixed(2)}`} />
    <StatCard title="Total Credits"  value={`₹ ${credits.toFixed(2)}`}  color="green" />
    <StatCard title="Total Debits"   value={`₹ ${debits.toFixed(2)}`}   color="red" />
    <StatCard title="Cashback"       value={`₹ ${cashback.toFixed(2)}`} />
</div>
```

Props can also pass **functions** — child calls parent's function:

```jsx
// parent passes function as prop
<TransactionForm onAddTransaction={addTransaction} />

// child calls it
function TransactionForm({ onAddTransaction }) {
    const handleSubmit = (e) => {
        e.preventDefault();
        onAddTransaction(amount, type);   // calls parent's function
    };
}
```

---

## Topic 4 — useState

State = data that **changes over time** and causes automatic UI re-render.

```jsx
// syntax
const [value, setValue] = useState(initialValue);
//     ↑ read    ↑ update

// replaces: document.getElementById("balance").textContent = "..."
// React updates the UI automatically when setValue is called
```

### Applied to wallet app — Dashboard stats

```jsx
function Dashboard() {
    const [balance,  setBalance]  = useState(1445.50);
    const [credits,  setCredits]  = useState(2500.00);
    const [debits,   setDebits]   = useState(1054.50);
    const [cashback, setCashback] = useState(150.00);

    const addTransaction = (amount, type) => {
        if (type === "credit") {
            setCredits(credits + amount);
            setBalance(balance + amount);
        } else {
            setDebits(debits + amount);
            setBalance(balance - amount);
        }
        // React automatically re-renders — no DOM manipulation needed!
    };
}
```

### Controlled inputs — form fields tied to state

```jsx
function TransactionForm({ onAddTransaction }) {
    const [amount, setAmount] = useState("");
    const [type,   setType]   = useState("credit");

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}  // controlled
            />
            <select value={type} onChange={(e) => setType(e.target.value)}>
                <option value="credit">Credit</option>
                <option value="debit">Debit</option>
            </select>
            <button type="submit">Add Transaction</button>
        </form>
    );
}
```

---

## Topic 5 — useEffect

Runs code **after component renders** — used for fetching data, subscriptions, side effects.

```jsx
useEffect(() => {
    // runs after render
}, [dependencies]);

// dependency array controls WHEN it runs:
[]           → runs ONCE on mount (like DOMContentLoaded)
[user]       → runs whenever user changes
(no array)   → runs after every render
```

### Applied to wallet app — load transactions on page load

```jsx
function Transactions() {
    const [transactions, setTransactions] = useState([]);
    const [loading,      setLoading]      = useState(true);

    useEffect(() => {
        async function fetchTransactions() {
            const response = await fetch("https://mockapi.io/transactions");
            const data     = await response.json();
            setTransactions(data);
            setLoading(false);
        }
        fetchTransactions();
    }, []);   // [] = runs once on mount

    if (loading) return <p>Loading transactions...</p>;

    return (
        <table>
            <tbody>
                {transactions.map(txn => (
                    <tr key={txn.id}>
                        <td>{txn.date}</td>
                        <td>{txn.type}</td>
                        <td>₹ {txn.amount}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
```

---

## Topic 6 — useContext

Shares state **globally** across all components — avoids prop drilling.

```
Without context — prop drilling:
App → Dashboard → Profile → UserCard
(user passed down at every level even if Dashboard doesn't use it)

With context — any component accesses directly:
App (provides user)
    ├── Navbar     → useUser() → gets user directly
    ├── Dashboard  → useUser() → gets user directly
    └── Profile    → useUser() → gets user directly
```

### Setup — 3 steps

**Step 1 — Create context** `UserContext.jsx`:

```jsx
import { createContext, useContext, useState } from "react";

export const UserContext = createContext(null);

// provider — wraps the whole app
export function UserProvider({ children }) {
    const [user, setUser] = useState(
        JSON.parse(localStorage.getItem("currentUser")) || null
    );
    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
}

// custom hook — convenience wrapper
export function useUser() {
    return useContext(UserContext);
}
```

**Step 2 — Wrap app** in `App.jsx`:

```jsx
import { UserProvider } from "./UserContext";

function App() {
    return (
        <UserProvider>
            <Router>
                <Navbar />
                <Routes>...</Routes>
            </Router>
        </UserProvider>
    );
}
```

**Step 3 — Consume in any component**:

```jsx
// Navbar
import { useUser } from "./UserContext";
function Navbar() {
    const { user, setUser } = useUser();
    // user available directly — no props needed
}

// Login — sets user after successful login
function Login() {
    const { setUser } = useUser();
    // after login:
    setUser(user);          // updates context globally
    navigate("/dashboard"); // redirect
}

// Transactions — filters by logged-in user
function Transactions() {
    const { user } = useUser();
    // filter: txn.userId === user.id
}
```

---

## Topic 7 — React Router

Navigation between pages without reload.

```jsx
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useNavigate } from "react-router-dom";

// App.jsx — define all routes
function App() {
    return (
        <UserProvider>
            <Router>
                <Navbar />
                <Routes>
                    <Route path="/login"    element={<Login />} />
                    <Route path="/register" element={<Register />} />

                    {/* protected — redirect to login if not logged in */}
                    <Route path="/dashboard"    element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
                    <Route path="/transactions" element={<ProtectedRoute><Transactions /></ProtectedRoute>} />
                    <Route path="/profile"      element={<ProtectedRoute><Profile /></ProtectedRoute>} />

                    <Route path="/" element={<Navigate to="/login" />} />
                </Routes>
            </Router>
        </UserProvider>
    );
}

// protected route — checks if user is logged in
function ProtectedRoute({ children }) {
    const { user } = useUser();
    return user ? children : <Navigate to="/login" />;
}
```

### Navigation in components

```jsx
// use Link instead of <a> — no page reload
<Link to="/dashboard">Dashboard</Link>

// use useNavigate for programmatic redirect
const navigate = useNavigate();
navigate("/dashboard");    // after login
navigate("/login");        // after logout
```







## Topic progression across 3 sessions

```
Session 1:
    What is React → Setup → JSX → Components → Props → StatCard

Session 2:
    useState → Controlled forms → TransactionForm → Login → Register

Session 3:
    useEffect → fetch data → useContext → UserProvider
    → React Router → ProtectedRoute → Full app connected
```






## Session 3 — Forms, Validation, MUI, State Management

### Form Validation — 3 approaches

**1. Manual validation**
```jsx
if (!email.includes("@")) {
    setError("Invalid email address");
}
```

**2. Formik + Yup**
```bash
npm install formik yup
```
```jsx
const RegisterSchema = Yup.object().shape({
    firstName:   Yup.string().required("First name is required"),
    email:       Yup.string().email("Invalid email").required(),
    password:    Yup.string().min(6).required(),
    accountType: Yup.string().oneOf(["Standard", "Premium"]).required()
});

<Formik
    initialValues={{ firstName: "", email: "", password: "", accountType: "" }}
    validationSchema={RegisterSchema}
    onSubmit={handleRegister}
>
    {() => (
        <Form>
            <Field name="firstName" className="form-control" placeholder="First Name" />
            <ErrorMessage name="firstName" component="div" className="text-danger" />
        </Form>
    )}
</Formik>
```

**3. React Hook Form + Zod (modern)**
```bash
npm install react-hook-form @hookform/resolvers zod
```
```jsx
const RegisterSchema = z.object({
    firstName:   z.string().min(1, "Required"),
    email:       z.string().email("Invalid email"),
    password:    z.string().min(6, "Min 6 characters"),
    accountType: z.enum(["Standard", "Premium"])
});

const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(RegisterSchema)
});

// in JSX
<input {...register("firstName")} className="form-control" />
{errors.firstName && <p className="text-danger">{errors.firstName.message}</p>}
```

---

### MUI (Material UI)
```bash
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/icons-material
```

Replaces Bootstrap classes with React components:

```jsx
// Bootstrap               →   MUI
<div class="container">   →   <Box sx={{ p: 3 }}>
<div class="row">         →   <Grid container spacing={2}>
<div class="col-md-3">    →   <Grid item xs={12} sm={6} md={3}>
<button class="btn">      →   <Button variant="contained">
<nav class="navbar">      →   <AppBar position="static">
<div class="card">        →   <Paper sx={{ p: 2 }}>
```

### Applied to Dashboard
```jsx
import { Box, Typography, Button, Grid, Paper } from "@mui/material";

function Dashboard() {
    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>Welcome to Wallet App</Typography>

            <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard title="Wallet Balance" value={`₹ ${balance.toFixed(2)}`} />
                </Grid>
                {/* repeat for credits, debits, cashback */}
            </Grid>

            <Button variant="contained" color="success" onClick={() => addTransaction(500, "credit")}>
                Add 500
            </Button>
            <Button variant="contained" color="error" onClick={() => addTransaction(200, "debit")}>
                Debit 200
            </Button>

            <Paper sx={{ p: 2, mb: 3 }}>
                <TransactionForm onAddTransaction={addTransaction} />
            </Paper>

            <Paper sx={{ p: 2 }}>
                <Transactions />
            </Paper>
        </Box>
    );
}
```

---

### Advanced State Management

#### useReducer — replaces multiple useState calls
```jsx
// when to use:
// useState    → 1-2 independent values
// useReducer  → 3+ related values updated together

const [walletState, dispatch] = useReducer(walletReducer, initialWalletState);

// one dispatch updates balance + credits + transactions atomically
dispatch({ type: "ADD_TRANSACTION", payload: { amount: 500, type: "credit" } });
```

```javascript
// walletReducer.js
function walletReducer(state, action) {
    switch (action.type) {
        case "ADD_TRANSACTION": {
            const { amount, type } = action.payload;
            if (type === "credit") {
                return {
                    ...state,
                    balance:  state.balance + amount,
                    credits:  state.credits + amount,
                    transactions: [
                        { id: Date.now(), amount, type, date: new Date().toISOString().split("T")[0] },
                        ...state.transactions
                    ]
                };
            } else {
                return { ...state, balance: state.balance - amount, debits: state.debits + amount };
            }
        }
        default: return state;
    }
}
```

#### Redux — centralized global store
```bash
npm install @reduxjs/toolkit react-redux
```

```javascript
// walletSlice.js
const walletSlice = createSlice({
    name: "wallet",
    initialState: { balance: 1000, credits: 2500, debits: 500, cashback: 80 },
    reducers: {
        addCredit: (state, action) => {
            state.credits  += action.payload;
            state.balance  += action.payload;
            state.cashback += action.payload * 0.02;
        },
        addDebit: (state, action) => {
            state.debits  += action.payload;
            state.balance -= action.payload;
        },
        resetWallet: () => initialState
    }
});
```

```jsx
// Dashboard — reading and writing Redux store
const { balance, credits, debits, cashback } = useSelector(state => state.wallet);
const dispatch = useDispatch();

dispatch(addCredit(500));
dispatch(addDebit(200));
```

#### Zustand — simplest of all three
```bash
npm install zustand
```

```jsx
// walletStore.js
const useWalletStore = create((set) => ({
    balance:  1000,
    credits:  2500,
    addCredit: (amount) => set(state => ({
        credits: state.credits + amount,
        balance: state.balance + amount
    })),
    addDebit: (amount) => set(state => ({
        debits:  state.debits + amount,
        balance: state.balance - amount
    }))
}));

// Dashboard — no Provider needed!
const { balance, credits, addCredit, addDebit } = useWalletStore();
```

---

## State Management — Final Comparison

| | useState | useReducer | Redux | Zustand |
|---|---|---|---|---|
| **Best for** | Simple values | Related values | Large apps | Any size |
| **Setup** | Zero | Zero | Store + Provider | Zero |
| **Global** | No | No | Yes | Yes |
| **Boilerplate** | None | Low | Medium | Minimal |
| **In wallet app** | Individual fields | Wallet stats | Full app state | Wallet stats |

---

## Complete Topic Progression

```
Session 1:
    What is React → Setup → JSX → Components → Props → useState
    → StatCard → TransactionForm → Login → Register

Session 2:
    useEffect → fetch on load → useContext → UserProvider
    → React Router → ProtectedRoute → Dynamic routes → Logout

Session 3:
    Form validation (manual → Formik/Yup → RHF/Zod)
    → MUI components → Event handling
    → useReducer → Redux → Zustand
```


# Flask Backend:

## Flask Sessions — Complete Summary

---

## What is Flask and Why

```
Before Flask:
React → MockAPI (someone else's server, limited control)

With Flask:
React → Flask (our server) → SQLite database
         ↑
         your Python code — same language you already know!
```

Benefits of having your own Flask backend:
- Custom business logic — fee calculations, balance checks, cashback
- Real database — data persists, not lost on refresh
- Security — sensitive operations handled on server
- Full control — your rules, your data

---

## Installation

```bash
pip install flask flask-cors flask-sqlalchemy
```

Verify everything installed:
```bash
pip show flask
pip show flask-sqlalchemy
pip show flask-cors
```

---

## Topic 1 — First Flask File

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)
# __name__ → tells Flask where the app lives
# Flask uses it to locate resources and templates

@app.route("/")
def home():
    return jsonify({ "message": "Wallet App API is running!" })

@app.route("/api/test")
def test():
    return jsonify({
        "status":  "ok",
        "version": "1.0",
        "message": "Flask backend connected"
    })

if __name__ == "__main__":
    app.run(debug=True)   # runs on http://localhost:5000
```

Run it:
```bash
python app.py
```

What you see in terminal:
```
* Serving Flask app 'app'
* Debug mode: on
WARNING: This is a development server.    ← ignore this, normal in dev
* Running on http://127.0.0.1:5000
* Restarting with stat
* Debugger is active!
* Debugger PIN: xxx-xxx-xxx
```

Every line explained:

```
* Serving Flask app 'app'         → found your app.py file
* Debug mode: on                  → auto-restarts on save
WARNING: development server       → safe to ignore during learning
* Running on http://127.0.0.1:5000 → your API is live here
* Restarting with stat            → file watcher is active
* Debugger PIN: 249-675-888       → only needed for browser debug
```

---

## Topic 2 — SQLAlchemy

### Core idea — Python class = database table

```
Python Class          Database Table
────────────          ──────────────
class User            users table
    id          →     id column
    first_name  →     first_name column
    last_name   →     last_name column
    password    →     password column

user = User(...)  →   one row in the table
```

### Setup

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]        = "sqlite:///test.db"
# sqlite:///test.db → creates test.db file in current folder
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
```

### Define a table

```python
class Student(db.Model):
    __tablename__ = "students"   # name of the table in database

    id   = db.Column(db.Integer,    primary_key=True)  # auto-increment
    name = db.Column(db.String(50), nullable=False)    # required text
    age  = db.Column(db.Integer)                       # optional number
    city = db.Column(db.String(50), default="Bangalore") # with default

    def __repr__(self):
        return f"Student({self.name}, {self.age})"
```

### Column types

```python
db.Column(db.Integer)        # whole number:  1, 2, 100
db.Column(db.Float)          # decimal:       1445.50
db.Column(db.String(50))     # text:          max 50 chars
db.Column(db.Text)           # long text:     no limit
db.Column(db.Boolean)        # true/false:    True or False
db.Column(db.DateTime)       # date and time

# column options
primary_key=True    # unique id, auto-increments
nullable=False      # required — cannot be empty
default="Standard"  # value used when not provided
unique=True         # no duplicates allowed
```

### Create table + add data

```python
# create tables — run once on startup
with app.app_context():
    db.create_all()
    print("Table created!")

# add data — staging + commit pattern
with app.app_context():
    s1 = Student(name="Vinod", age=25, city="Bangalore")
    s2 = Student(name="Amar",  age=22, city="Mumbai")
    s3 = Student(name="Priya", age=24)   # city defaults to Bangalore

    db.session.add(s1)    # stage
    db.session.add(s2)
    db.session.add(s3)
    db.session.commit()   # save permanently to database
    print("Data added!")
```

### All query methods

```python
# READ
User.query.all()                              # get all rows
db.session.get(User, 1)                       # get by id (modern way)
User.query.first()                            # get first row
User.query.count()                            # count total rows

# FILTER
User.query.filter_by(city="Bangalore").all()  # exact match
User.query.filter(User.age > 20).all()        # condition
User.query.filter_by(city="B").first()        # first match only
User.query.filter(
    User.age > 20,
    User.city == "Bangalore"
).all()                                       # multiple conditions

# ORDER
User.query.order_by(User.age).all()           # ascending
User.query.order_by(User.age.desc()).all()    # descending

# LIMIT
User.query.limit(5).all()                     # only 5 rows

# ADD
db.session.add(new_user)
db.session.commit()

# UPDATE — no add() needed
user = db.session.get(User, 1)
user.first_name = "Updated"
db.session.commit()

# DELETE
user = db.session.get(User, 1)
db.session.delete(user)
db.session.commit()
```

---

## Topic 3 — Relationships

One user has many transactions:

```python
class User(db.Model):
    __tablename__ = "users"
    id           = db.Column(db.Integer,    primary_key=True)
    first_name   = db.Column(db.String(50), nullable=False)

    # relationship → gives user.transactions as a list
    transactions = db.relationship("Transaction", backref="user", lazy=True)
    #                               ↑ model name    ↑ txn.user     ↑ load on demand


class Transaction(db.Model):
    __tablename__ = "transactions"
    id      = db.Column(db.Integer, primary_key=True)
    amount  = db.Column(db.Float,   nullable=False)

    # foreign key — links each transaction to a user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    #                                              ↑ tablename.column
```

Using the relationship:

```python
with app.app_context():
    user = db.session.get(User, 1)
    print(user.transactions)       # [<Transaction 1>, <Transaction 2>]

    txn = db.session.get(Transaction, 1)
    print(txn.user.first_name)     # "Vinod"
```

---

## Topic 4 — `to_dict()` method

SQLAlchemy objects can't be sent as JSON directly. `to_dict()` converts them:

```python
class User(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    age        = db.Column(db.Integer)
    city       = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id":         self.id,
            "first_name": self.first_name,
            "age":        self.age,
            "city":       self.city
            # password deliberately excluded — like Python encapsulation
        }

# in a route:
user = db.session.get(User, 1)
return jsonify(user.to_dict())            # one user

users = User.query.all()
return jsonify([u.to_dict() for u in users])  # list of users
```

---

## Topic 5 — Flask Routes (REST API)

### What is a REST API

```
REST = Representational State Transfer
     = standard way of building APIs using HTTP methods

GET    → fetch data      (read)
POST   → add new data    (create)
PUT    → update data     (update)
DELETE → remove data     (delete)

Each URL = one resource
/users          → all users
/users/1        → one specific user
/users/1/transactions → transactions for user 1
```

### All routes implemented

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]        = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id         = db.Column(db.Integer,    primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    age        = db.Column(db.Integer)
    city       = db.Column(db.String(50), default="Bangalore")
    transactions = db.relationship("Transaction", backref="user", lazy=True)

    def to_dict(self):
        return { "id": self.id, "first_name": self.first_name,
                 "age": self.age, "city": self.city }


class Transaction(db.Model):
    __tablename__ = "transactions"
    id      = db.Column(db.Integer, primary_key=True)
    amount  = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return { "id": self.id, "amount": self.amount, "user_id": self.user_id }


# ── HOME ──────────────────────────────────────────
@app.route("/")
def home():
    return "Wallet API is running!"


# ── USER ROUTES ───────────────────────────────────

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = db.session.get(User, id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data or "first_name" not in data:
        return jsonify({"error": "first_name is required"}), 400

    user = User(
        first_name = data["first_name"],
        age        = data.get("age"),
        city       = data.get("city", "Bangalore")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.first_name = data.get("first_name", user.first_name)
    user.age        = data.get("age",        user.age)
    user.city       = data.get("city",       user.city)
    db.session.commit()
    return jsonify(user.to_dict())


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {id} deleted"})


# ── TRANSACTION ROUTES ────────────────────────────

@app.route("/users/<int:id>/transactions", methods=["GET"])
def get_user_transactions(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify([t.to_dict() for t in user.transactions])


@app.route("/users/<int:id>/transactions", methods=["POST"])
def add_transaction(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data or "amount" not in data:
        return jsonify({"error": "amount is required"}), 400

    txn = Transaction(amount=data["amount"], user=user)
    db.session.add(txn)
    db.session.commit()
    return jsonify(txn.to_dict()), 201


# ── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

---

## Topic 6 — Testing with Thunder Client

### Open Thunder Client

```
VS Code left sidebar → click ⚡ thunderbolt icon
or
Ctrl+Shift+P → type "Thunder Client" → Enter
Click "New Request"
```

### How to set up each request

```
┌─────────────────────────────────────────────────┐
│  POST ▼ │ http://127.0.0.1:5000/users │  Send  │
├─────────────────────────────────────────────────┤
│  Query   Headers   Auth   Body  ← click Body    │
├─────────────────────────────────────────────────┤
│  None   Form   Form-encode   XML   JSON  ← JSON │
├─────────────────────────────────────────────────┤
│  {  ← paste your JSON body here                 │
│      "first_name": "Vinod",                     │
│      "age": 25                                  │
│  }                                              │
└─────────────────────────────────────────────────┘
```

### All 10 tests in order

```
Test 1  GET    /users                      → []
Test 2  POST   /users                      → add Vinod   → {id:1}
Test 3  POST   /users                      → add Amar    → {id:2}
Test 4  GET    /users                      → [Vinod, Amar]
Test 5  GET    /users/1                    → Vinod only
Test 6  GET    /users/99                   → 404 error
Test 7  PUT    /users/1                    → update city
Test 8  POST   /users/1/transactions       → add ₹500
Test 9  GET    /users/1/transactions       → [500 txn]
Test 10 DELETE /users/2                    → Amar deleted
```

### Status codes to know

```
200 → OK          — GET, PUT, DELETE success
201 → Created     — POST success (new item created)
400 → Bad Request — missing required field
404 → Not Found   — id doesn't exist
405 → Method Not Allowed — wrong HTTP method used
500 → Server Error — crash in your Flask code
```

---

## How Python wallet code maps to Flask

| Python file | Flask equivalent |
|---|---|
| `class User` | `class User(db.Model)` |
| `self.first_name = first_name` | `first_name = db.Column(db.String(50))` |
| `users.json` file | `data.db` SQLite file |
| `storage_service.py save_user()` | `db.session.add() + db.session.commit()` |
| `storage_service.py load_user()` | `User.query.filter_by(...).first()` |
| `wallet_service.py account_history()` | `GET /users/<id>/transactions` |
| `wallet_service.py add_transaction()` | `POST /users/<id>/transactions` |

---

## Run both servers together

```bash
# Terminal 1 — Flask backend
cd wallet-backend
python app.py
# running at http://127.0.0.1:5000

# Terminal 2 — React frontend
cd wallet-react
npm run dev
# running at http://localhost:5173
```

---

## Next steps — wallet app routes

The current `app.py` has basic user and transaction routes. The full wallet `app.py` (already created) adds:

```
POST /api/login                        → check credentials
PUT  /api/users/<id>/password          → change password
POST /api/transactions                 → add with fee + balance update
GET  /api/transactions?userId=1        → filter by user
GET  /api/transactions/summary?userId=1 → totals
DELETE /api/transactions/<id>          → delete + reverse balance
```

Once all Thunder Client tests pass on the basic routes, swap to the wallet `app.py` and test those routes next.