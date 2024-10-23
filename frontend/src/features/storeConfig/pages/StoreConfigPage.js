import React from "react";

// Importing components for display and configuration
import PictureAndDescriptionField from "../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField";
import StoreOpeningTimesConfig from "../components/StoreOpeningTimesConfig";
import BikeList from "../../bikeList/components/BikeList";

// Importing hooks for routing and translation
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useNavigate } from 'react-router-dom';

// Importing a text field component
import SingleLineTextField from "../../../components/display/SingleLineTextField";

// Mock data for stores (to be replaced with actual fetching logic)
let stores = [
    {

        id: 1,
        name: 'Store 1',
        image: require('../../../assets/images/store1.jpg'),
        description: 'This is a description of Store 1',
        address: 'Musterstraße 123, 76137 Karlsruhe'
    },
    {
        id: 2,
        name: 'Store 2',
        image: require('../../../assets/images/store1.jpg').default,
        description: 'This is a description of Store 2',
        address: 'Musterstraße 123, 76137 Karlsruhe'
    },
    {
        id: 3,
        name: 'Store 3',
        image: null,
        description: 'This is a description of Store 3',
        address: 'Musterstraße 123, 76137 Karlsruhe'
    }
]

// Main component for configuring store settings
const StoreConfigPage = () => {

    // Hook for translation
    const { t } = useTranslation();

    // Extracting store ID from URL parameters
    const { id } = useParams();
    // Finding the store object based on the ID
    const store = stores.find(s => s.id === parseInt(id));

    // Hook for navigation
    const navigate = useNavigate();

    // Handler for bookings button click
    const handleBookingsClick = () => {
        // Logic for handling bookings click (to be implemented)
    };

    return (
        <div>
            {/* Displaying store picture and description */}
            <PictureAndDescriptionField 
                image={store.image} 
                description={store.description} 
            />
            {/* Configuring store opening times */}
            <StoreOpeningTimesConfig />
            {/* Displaying list of bikes */}
            <BikeList />
            {/* Single line text field for store name */}
            <SingleLineTextField value={store.name} />
        </div>
    );
};

export default StoreConfigPage;