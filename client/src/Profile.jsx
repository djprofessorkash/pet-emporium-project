import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Profile = ({currentUser}) => {
    const navigate = useNavigate();

    const [userAssociatedDogs, setUserAssociatedDogs] = useState([]);

    useEffect(() => {
		fetch(`/api/users/${currentUser.id}/dogs`)
		.then((response) => response.json())
        .then((data) => setUserAssociatedDogs([...data]));
	}, []);

    return (
        <div className={"mainContainer"}>
            <div className={"titleContainer"}>
                Profile: <br /><small><i>{currentUser.username}</i></small>
            </div>
            <br />
            <h3>Your Dogs:</h3>
                {
                    userAssociatedDogs.map((adoptedDog) => <div><button className={"dogContainerInProfile"} >{adoptedDog.name} ({adoptedDog.breed})</button></div>)
                }
            <div className={"buttonContainer"}>
                <input className={"inputButton"} type="button" onClick={() => navigate("/")} value="HOME" />
            </div>
        </div>
    )
}

export default Profile;