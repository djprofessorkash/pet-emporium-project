import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
    const navigate = useNavigate();

    const [allDogs, setAllDogs] = useState([]);

    useEffect(() => {
		fetch("/api/dogs")
		.then((response) => response.json())
        .then((data) => setAllDogs([...data]));
	}, []);

    const renderAdoptabilityStatus = (eachDog) => {
        console.log(eachDog)
        if (eachDog.is_adoptable === true) {
            return "Eligible for Adoption"
        } else {
            return "Currently Adopted"
        }
    }

    const handleDogDeletionOnClick = () => {
        return
    }

    return (
        <div className={"mainContainer"}>
            <div className={"titleContainer"}>
                Administrative Panel
            </div>
            <div>
                <h3>All Dogs:</h3>
                {
                    allDogs.map((eachDog) => <div><button>Delete</button><button>Edit</button><button>Process Adoption</button><p>{eachDog.name} ({eachDog.breed}) [STATUS: {renderAdoptabilityStatus(eachDog)}]</p></div>)
                }
            </div>
            <div className={"buttonContainer"}>
                <input className={"inputButton"} type="button" onClick={() => navigate("/")} value="HOME" />
            </div>
        </div>
    )
}

export default Dashboard;