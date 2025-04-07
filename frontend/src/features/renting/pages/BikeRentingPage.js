// Page of singular Bike
// Consists of a Name, Image, Description and Information about the store it belongs to
// Also has BikeCalendar which is component to make a reservation
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useParams } from 'react-router-dom';
import ImageAndDescriptionField from '../../../components/display/imageAndDescriptionField/ImageAndDescriptionField';
import TextField from '../../../components/display/TextField';
import BikeCalendar from '../../renting/components/calendar/BikeCalendar';
import { ID } from '../../../constants/URIs/General';
import { AVAILABILITY_OF_BIKE, BIKE_BY_ID, POST_BOOKING, STORE_BY_BIKE_ID } from '../../../constants/URIs/RentingURIs';
import { ERR_FETCHING_BIKE, ERR_FETCHING_STORE } from '../../../constants/messages/ErrorMessages';
import { STORE_PAGE_OF_BIKE } from '../../../constants/URLs/Navigation';
import { getCookie } from '../../../services/Cookies';
import { useNotification } from '../../../components/notifications/NotificationContext';

// Standard page for a Bike

// TODO add equipment selection
// TODO users that arent locked in should also be able to see this page

const BikeRentingPage = () => {

    const { t } = useTranslation(); // Translation hook
    const { showNotification } = useNotification();

    const navigate = useNavigate(); // Navigation hook

    const token = getCookie('token'); // Get token from cookies

    const bikeId = useParams().bike; // Get bike ID from URL parameters
    const [bike, setBike] = useState(); // State to store bike data
    const [store, setStore] = useState(); // State to store store data
    const [availabilities, setAvailabilities] = useState([]); // State to store availability data

    const [selectedStartDate, setSelectedStartDate] = useState(null);
    const [selectedEndDate, setSelectedEndDate] = useState(null);

    const [openingTimes, setOpeningTimes] = useState({});

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
                setOpeningTimes({
                    mon: data.mon_opened,
                    tue: data.tue_opened,
                    wed: data.wed_opened,
                    thu: data.thu_opened,
                    fri: data.fri_opened,
                    sat: data.sat_opened,
                    sun: data.sun_opened
                });
            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error); // Log error if fetching store fails
            });
    }

    const fetchAvailabilities = async () => {
        const response = await fetch(AVAILABILITY_OF_BIKE.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        });
        const data = await response.json();
        setAvailabilities(data);
    };


    const postBooking = async () => {
        if (!selectedStartDate || !selectedEndDate) {
            showNotification(t('select_dates_first'), 'error');
            return;
        }
        const payload = {
            begin: selectedStartDate.toLocaleDateString('en-CA'), // format date to 'YYYY-MM-DD'
            end: selectedEndDate.toLocaleDateString('en-CA'),
            equipment: []
        };
        try {
            const response = await fetch(POST_BOOKING.replace(ID, bikeId), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                showNotification(t('booking_successful'), 'success');
                setSelectedStartDate(null);
                setSelectedEndDate(null);
                await fetchAvailabilities();
            } else {
                const error = await response.json();
                throw new Error(error.detail);
            }
        } catch (error) {
            showNotification(`${t('booking_failed')}: ${error.message}`, 'error');
        }
    };

    const handleBookClick = () => {
        postBooking(); // Call function to post booking
    }

    // Fetch bike and store data when component mounts
    useEffect(() => {
        fetchBike();
        fetchStore();
        fetchAvailabilities();
    }, [])

    // Handle click on store button
    const handleStoreClick = () => {
        navigate(STORE_PAGE_OF_BIKE.replace(ID, bike.id)) // Navigate to store page by bike ID
    }

    return (
        <> {bike && store &&
            <>
                <h1>{bike?.name}</h1> {/* Display bike name */}

                <ImageAndDescriptionField editable={false} imageValue={bike?.image} descriptionValue={bike?.description} />
                {/* Display store address */}
                <TextField editable={false} value={store?.address} singleLine={true} title='address' />

                <div className='button-container'>
                    <button type='button' className='button regular' onClick={handleStoreClick}>{store?.name}</button> {/* Button to navigate to store page */}
                </div>

                {/* Display bike calendar for reservations */}
                <BikeCalendar
                    storeOpeningDays={openingTimes}
                    availabilities={availabilities}
                    selectedStartDate={selectedStartDate}
                    setSelectedStartDate={setSelectedStartDate}
                    selectedEndDate={selectedEndDate}
                    setSelectedEndDate={setSelectedEndDate}
                />

                <div className='button-container'>
                    <button onClick={handleBookClick} className="button accent">{t('book_now')}</button>
                </div>
            </>
        }
        </>
    );
};

export default BikeRentingPage;