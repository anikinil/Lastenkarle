// Page of singular Bike
// Consists of a Name, Image, Description and Information about the store it belongs to
// Also has BikeCalendar which is component to make a reservation
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useParams } from 'react-router-dom';
import ImageAndDescriptionField from '../../../components/display/imageAndDescriptionField/ImageAndDescriptionField';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import BikeCalendar from '../../renting/components/calendar/BikeCalendar';
import { ID } from '../../../constants/URIs/General';
import { BIKE_BY_ID, STORE_BY_BIKE_ID } from '../../../constants/URIs/RentingURIs';
import { ERR_FETCHING_BIKE, ERR_FETCHING_STORE } from '../../../constants/ErrorMessages';
import { STORE_PAGE } from '../../../constants/URLs/Navigation';

//Standard page for a Bike
//TODO: organize Images
//TODO: Add bike description
//TODO: Add Store information
//TODO: Add calandar as availability overview

// TODO add equipment selection (Ilja)

const BikeRentingPage = () => {
    const { t } = useTranslation(); // Translation hook
    const navigate = useNavigate(); // Navigation hook

    const bikeId = useParams().bike; // Get bike ID from URL parameters
    const [bike, setBike] = useState(); // State to store bike data
    const [store, setStore] = useState(); // State to store store data

    // fetch bike
    const fetchBike = () => {
        fetch(BIKE_BY_ID.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                setBike(data); // Set bike data to statec
            })
            .catch(error => {
                console.error(ERR_FETCHING_BIKE, error); // Log error if fetching bike fails
            });
    }

    // fetch store
    const fetchStore = () => {
        fetch(STORE_BY_BIKE_ID.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                setStore(data); // Set store data to state
            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error); // Log error if fetching store fails
            });
    }

    // Fetch bike and store data when component mounts
    useEffect(() => {
        fetchBike();
        fetchStore();
    }, [])

    // Handle click on store button
    const handleStoreClick = () => {
        navigate(STORE_PAGE.replace(ID, bike.id)) // Navigate to store page by bike ID
    }

    return (
        <> {bike && store &&
            <>
                <h1>{bike?.name}</h1> {/* Display bike name */}

                <ImageAndDescriptionField editable={false} imageValue={bike?.image} descriptionValue={bike?.description} />
                {/* Display store address */}
                <SingleLineTextField editable={false} value={store?.address} title='address' />

                <div className='button-container'>
                    <button type='button' className='button regular' onClick={handleStoreClick}>{store?.name}</button> {/* Button to navigate to store page */}
                </div>

                {/* Display bike calendar for reservations */}
                <BikeCalendar />
            </>
        }
        </>
    );
};

export default BikeRentingPage;