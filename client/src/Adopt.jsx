import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Adopt = () => {
    const navigate = useNavigate();

    const [adoptableDogs, setAdoptableDogs] = useState([]);

    useEffect(() => {
		fetch("/api/adopt")
		.then((response) => response.json())
        .then((data) => setAdoptableDogs([...data]));
	}, []);

    return (
        <div className={"mainContainer"}>
            <div className={"titleContainer"}>
                Adopt a Pet Today!
            </div>
            <div>
                <h3>Currently Adoptable Dogs:</h3>
                {
                    adoptableDogs.map((adoptableDog) => <div><button>{adoptableDog.name} ({adoptableDog.breed})</button></div>)
                }
            </div>
            <div className={"buttonContainer"}>
                <input className={"inputButton"} type="button" onClick={() => navigate("/")} value="HOME" />
            </div>
        </div>
    )
}

export default Adopt;