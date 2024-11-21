// Page of singular Bike
// Consists of a Name, Picture, Description and Information about the store it belongs to
// Also has BikeCalendar which is component to make a reservation
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useParams } from 'react-router-dom';
import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import BikeCalendar from '../../booking/components/calendar/BikeCalendar';
import { ID } from '../../../constants/URIs/General';
import { BIKE_BY_ID, STORE_BY_BIKE_ID } from '../../../constants/URIs/BookingURIs';
import { ERR_FETCHING_BIKE, ERR_FETCHING_STORE } from '../../../constants/ErrorMessages';
import { getCookie } from '../../../services/Cookies';

const BikeBookingPage = () => {
    const { t } = useTranslation(); // Translation hook
    const navigate = useNavigate(); // Navigation hook

    const bikeId = useParams().bike; // Get bike ID from URL parameters
    const [bike, setBike] = useState(); // State to store bike data
    const [store, setStore] = useState(); // State to store store data

    const token = getCookie('token'); // Get authentication token from cookies

    // fetch bike
    const fetchBike = () => {
        fetch(BIKE_BY_ID.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        })
            .then(response => response.json())
            .then(data => {
                setBike(data); // Set bike data to state
                console.log(data);
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
                'Authorization': `Token ${token}`,
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
        navigate(`/store/${bike.store}`) // Navigate to store page
    }

    return (
        <>
            <h1>{bike?.name}</h1> {/* Display bike name */}

            {/* Display bike picture and description */}
            <PictureAndDescriptionField editable={false} object={bike} />
             {/* Display store address */}
            <SingleLineTextField editable={false} value={store?.address} title='address' />

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleStoreClick}>{store?.name}</button> {/* Button to navigate to store page */}
            </div>

            {/* Display bike calendar for reservations */}
            <BikeCalendar />
        </>
    );
};

export default BikeBookingPage;