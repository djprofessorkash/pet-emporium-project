import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
    const navigate = useNavigate();

    const [allDogs, setAllDogs] = useState([]);
    const [currentDogNameForNewEntry, setCurrentDogNameForNewEntry] = useState("");
    const [currentDogBreedForNewEntry, setCurrentDogBreedForNewEntry] = useState("");

    useEffect(() => {
		fetch("/api/dogs")
		.then((response) => response.json())
        .then((data) => setAllDogs([...data]));
	}, []);

    const renderAdoptabilityStatus = (eachDog) => {
        if (eachDog.is_adoptable === true) {
            return "Eligible for Adoption"
        } else {
            return "Currently Adopted"
        }
    }

    const handleDogDeletionOnClick = (dog) => {
        console.log(`Dog deletion triggered on ${dog.id}.`)
        fetch(`/api/dogs/${dog.id}`, {
            method: "DELETE",
        })
        // No response from backend due to Status Code 204 invocation.
        .then((result) => {
            console.log(result);
            setAllDogs(allDogs.filter(dogElement => dogElement.id !== dog.id))
        })
    }

    const handleDogEditOnClick = (dog) => {
        // TODO: Complete function to edit dog. (Requires modal form.)
        console.log(`Dog edit triggered on ${dog.id}.`)
    }

    const handleDogAdoptionOnClick = (dog) => {
        // TODO: Complete function to process adoption to specific user. (Requires significant backend and frontend scaling.)
        console.log(`Dog adoption to user triggered on ${dog.id}.`)
    }

    const handleNewDogSubmissionOnClick = (event) => {
        // TODO: Complete function to create new dog. (Requires POST-powered form submission.)
        event.preventDefault()
        console.log(`Dog submission form triggered for new dog.`)
        console.log(` >> New dog's name: ${currentDogNameForNewEntry}.`)
        console.log(` >> New dog's breed: ${currentDogBreedForNewEntry}.`)
        fetch("api/dogs", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "name": currentDogNameForNewEntry,
                "breed": currentDogBreedForNewEntry
            })
        })
        .then((response) => response.json())
        .then((result) => {
            console.log(result)
            setAllDogs([...allDogs, result])
        })
    }

    return (
        <div className={"mainContainer"}>
            <div className={"titleContainer"}>
                Administrative Panel
            </div>
            <br />
            <div>
                <h2>Add a New Dog</h2>
                <div className={"inputFormContainer"}>
                <form onSubmit={handleNewDogSubmissionOnClick}>
                    <label>Dog's Name</label>
                    <input type="text" onChange={(event) => setCurrentDogNameForNewEntry(event.target.value)}></input>
                    <br />
                    <label>Dog's Breed</label>
                    <input type="text" onChange={(event) => setCurrentDogBreedForNewEntry(event.target.value)}></input>
                    <button type="submit">Submit</button>
                </form>
                </div>
            </div>
            <br />
            <div>
                <h2>All Dogs:</h2>
                {
                    allDogs.map((eachDog) => <div>
                            <p>
                                <button className={"deleteOnClick"} onClick={() => handleDogDeletionOnClick(eachDog)}>X</button>
                                <button className={"editOnClick"} onClick={() => handleDogEditOnClick(eachDog)}>EDIT</button>
                                {eachDog.name} (<i>{eachDog.breed}</i>) [STATUS: <b>{renderAdoptabilityStatus(eachDog)}</b>] 
                                <button className={"processAdoptionOnClick"} onClick={() => handleDogAdoptionOnClick(eachDog)}>Process Adoption</button>
                            </p>
                        </div>)
                }
            </div>
            <div className={"buttonContainer"}>
                <input className={"inputButton"} type="button" onClick={() => navigate("/")} value="HOME" />
            </div>
        </div>
    )
}

export default Dashboard;