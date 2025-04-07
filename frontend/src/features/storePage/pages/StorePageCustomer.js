// Page of a singular store
// Consists of Name, Image, Description and Information
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import i18n from 'i18next';

import { useParams } from 'react-router-dom';
import TextField from '../../../components/display/TextField';
import { ERR_FETCHING_STORE } from '../../../constants/messages/ErrorMessages';
import { STORE_BY_BIKE_ID } from '../../../constants/URIs/RentingURIs';
import { ID } from '../../../constants/URIs/General';

const getLocalizedWeekdays = () => {
    const locale = i18n.language;
    const baseDate = new Date(Date.UTC(2022, 7, 1)); // just a random Monday on the 1st of August 2022
    return Array.from({ length: 7 }).map((_, i) => {
        const date = new Date(baseDate);
        date.setDate(baseDate.getDate() + i);
        return date.toLocaleDateString(locale, { weekday: 'long' });
    });
};

const StorePageCustomer = () => {
    const { t } = useTranslation(); // Translation hook

    const bikeId = useParams().bike;
    const [store, setStore] = useState(); // State to hold store data
    const [openingTimes, setOpeningTimes] = useState([]); // State to hold opening times data

    // Function to fetch store data from the server
    const fetchStore = () => {
        fetch(STORE_BY_BIKE_ID.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json()) // Parse JSON response
            .then(data => {
                setStore(data); // Set store data to state
                setOpeningTimes([
                    { opened: data.mon_opened, open: data.mon_open, close: data.mon_close },
                    { opened: data.tue_opened, open: data.tue_open, close: data.tue_close },
                    { opened: data.wed_opened, open: data.wed_open, close: data.wed_close },
                    { opened: data.thu_opened, open: data.thu_open, close: data.thu_close },
                    { opened: data.fri_opened, open: data.fri_open, close: data.fri_close },
                    { opened: data.sat_opened, open: data.sat_open, close: data.sat_close },
                    { opened: data.sun_opened, open: data.sun_open, close: data.sun_close },
                ]);

            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error); // Log error if fetching fails
            });
    }

    // Fetch store data when component mounts
    useEffect(() => {
        fetchStore();
    }, []); // Empty dependency array ensures this runs only once

    return (
        <> {store &&
            <>
                <h1>{store?.name}</h1> {/* Display store name */}

                {/* NOTE crrently no image and description of store stored at backend */}
                {/* <ImageAndDescriptionField editable={false} imageValue={store?.image} descriptionValue={store?.description} /> */}
                
                <TextField editable={false} value={store?.address} singleLine={true} title={t('address')} /> {/* Display store address */}

                {openingTimes.map((day, key) => {
                    const localizedWeekdays = getLocalizedWeekdays();
                    const weekday = localizedWeekdays[key];
                    const openingTime = day.opened ? `${day.open} - ${day.close}` : t('closed');
                    let text;
                    if (day.opened) { text = `${weekday}: ${openingTime}`}
                    else { text = `${weekday}: ${t('closed')}` }
                    return <p key={key}>{text}</p>;
                })

                }
            </>
        }
        </>
    );
};

export default StorePageCustomer;