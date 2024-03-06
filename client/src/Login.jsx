import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = ({handleLogin, loggedIn, setLoggedIn, username, setUsername}) => {
    const [password, setPassword] = useState("");

    const navigate = useNavigate();

    const handleButtonClick = () => {
        handleLogin(username, password)
        .then((result) => {
            console.log(result);
            if (result === true) {
                alert("Login successful!");
                navigate("/");
            } else {
                alert("Login failed. Please try again.");
            }
        });
    }

    return (
        <div className={"mainContainer"}>
            <div className={"titleContainer"}>
                <div>Sign in to your profile</div>
            </div>
            <br />
            <br />
            <div className={"inputContainer"}>
                <input
                type="text"
                value={username}
                placeholder="Enter your username here"
                onChange={(event) => {setUsername(event.target.value); console.log(event.target.value)}}
                required
                className={"inputBox"}
                />
                {/* <label className="errorLabel">{usernameError}</label> */}
            </div>
            <br />
            <div className={"inputContainer"}>
                <input
                type="password"
                value={password}
                placeholder="Enter your password here"
                onChange={(event) => {setPassword(event.target.value); console.log(event.target.value)}}
                required
                className={"inputBox"}
                />
                {/* <label className="errorLabel">{passwordError}</label> */}
            </div>
            <br />
            <div className={"inputContainer"}>
                <input className={"inputButton"} type="button" onClick={handleButtonClick} value={"LOGIN"} />
            </div>
            </div>
    )
}

export default Login;