import { BrowserRouter, Route, Routes } from "react-router-dom";
import React, { useState, useEffect } from "react";
import Home from "./Home";
import Login from "./Login";
import "./App.css";

function App() {
	const [username, setUsername] = useState(null);
	const [currentUser, setCurrentUser] = useState(null);
	const [loggedIn, setLoggedIn] = useState(false);
	const [isAdministrator, setIsAdministrator] = useState(false);

	useEffect(() => {
		fetch("/check_session")
		.then((response) => {
			if (response.ok) {
				response.json().then(
				(user) => {
					setCurrentUser(user)
					setLoggedIn(true);
					if (user.is_admin === true) {
					setIsAdministrator(true);
					}
				}
				);
			} else {
			console.log("No user logged in.");
			}
		});
	}, []);

	const handleLogin = async (username, password) => {
		const response = await fetch("/login", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ 
				"username": username,
				"password": password
			}),
		});

		if (response.ok) {
			const result = await response.json();
			setLoggedIn(true);
			setUsername(result.username);
			if (result.is_admin === true) {
			setIsAdministrator(true);
			}
			return true;
		} else {
			const errorData = await response.json().catch(() => null); 
			console.log("ERROR:", errorData);
			return false;
		}
	};

	const handleLogout = async () => {
		const response = await fetch("/logout", {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json",
		},
		});
		
		if (response.ok) {
		console.log("Logout successful.")
		} else {
		console.log("Logout failed");
		}
		setLoggedIn(false);
		setCurrentUser(null);
		setIsAdministrator(false);
	};

	return (
		<div className="App">
		<BrowserRouter>
			<Routes>
			<Route path="/" element={<Home handleLogout={handleLogout} currentUser={currentUser} loggedIn={loggedIn} isAdministrator={isAdministrator} />} />
			<Route path="/login" element={<Login handleLogin={handleLogin} loggedIn={loggedIn} setLoggedIn={setLoggedIn} username={username} setUsername={setUsername} />} />
			<Route path="/profile" element={<div>This is the profile page.</div>} />
			<Route path="/adopt" element={<div>This is the dog adoptions page.</div>} />
			<Route path="/dashboard" element={<div>This is the admin dashboard page for dog data.</div>} />
			</Routes>
		</BrowserRouter>
		</div>
	);
}

export default App;
