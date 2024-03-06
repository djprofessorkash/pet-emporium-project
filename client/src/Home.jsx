import React from "react";
import { useNavigate } from "react-router-dom";

const Home = ({handleLogout, currentUser, loggedIn, isAdministrator}) => {
    const navigate = useNavigate();

    console.log("Current User: ", currentUser);

    const handleUserAuthToggleButton = () => {
        if (loggedIn) {
            // Perform logout using fetch() on backend route for logout. 
            handleLogout()
        } else {
            navigate("/login");
        }
    }
        
    const handleUserProfileButton = () => {
        navigate("/profile");
    }

    const handleAdoptablePetsButton = () => {
        navigate("/adopt");
    }

    const handlePetDashboardButton = () => {
        navigate("/dashboard");
    }

    // I hate React.
    const renderUsername = () => {
        if (loggedIn) {
            if (currentUser == null) {
                return "Hello, user!";
            } else {
                return `Hello, @${currentUser.username}!`;
            }
        } else {
            return "Welcome!";
        }
    }

    return (
        <div className="mainContainer">
            <div className={"titleContainer"}>
                {renderUsername()} 
            </div>
            <div className={"buttonContainer"}>
                <div>
                    {loggedIn ? <input className={"inputButton"} type="button" onClick={handleUserProfileButton} value="PROFILE" /> : null}
                    {loggedIn ? <input className={"inputButton"} type="button" onClick={handleAdoptablePetsButton} value="ADOPT A PET" /> : null}
                    {isAdministrator ? <input className={"inputButton"} type="button" onClick={handlePetDashboardButton} value="ADMIN DASHBOARD" /> : null}
                </div>
            </div>
            <div className={"buttonContainer"}>
                <input
                className={"inputButton"}
                type="button"
                onClick={handleUserAuthToggleButton}
                value={loggedIn ? "LOG OUT" : "LOG IN"}
                />
            </div>
        </div>
    )
}

export default Home;