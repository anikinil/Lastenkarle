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
import { ID } from "../../../constants/URIs/General";
import { STORE_NAME, STORE_PAGE_BY_STORE_NAME } from "../../../constants/URIs/ManagerURI";

// Mock data for stores (to be replaced with actual fetching logic)
// let stores = [
//     {

//         id: 1,
//         name: 'Store 1',
//         image: require('../../../assets/images/store1.jpg'),
//         description: 'This is a description of Store 1',
//         address: 'Musterstraße 123, 76137 Karlsruhe'
//     },
//     {
//         id: 2,
//         name: 'Store 2',
//         image: require('../../../assets/images/store1.jpg').default,
//         description: 'This is a description of Store 2',
//         address: 'Musterstraße 123, 76137 Karlsruhe'
//     },
//     {
//         id: 3,
//         name: 'Store 3',
//         image: null,
//         description: 'This is a description of Store 3',
//         address: 'Musterstraße 123, 76137 Karlsruhe'
//     }
// ]

// TODO make sure, storeName is passed to this component as parameter

// page for the configuration of an existing store
const StoreConfigPage = () => {

    const { t } = useTranslation();

    // Extracting store name from URL parameters
    const { storeName } = useParams();
    // State to hold store data
    const [store, setStore] = useState();

    const fetchStore = () => {
        fetch(STORE_PAGE_BY_STORE_NAME.replace(STORE_NAME, storeName))
            .then(response => response.json())
            .then(data => {
                setStore(data);
            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error);
            });
    }

    useEffect(() => {
        fetchStore();
    }, [])

    const handleAddressChange = (value) => {
        setNewAddress(value)
    }

    // Hook for navigation
    const navigate = useNavigate();

    return (
        <div>
            {/* Displaying store picture and description */}
            <PictureAndDescriptionField 
                image={store.image} 
                description={store.description} 
            />
            <SingleLineTextField editable={true} value={store.address} title={'address'} onChange={handleAddressChange}/>
            {/* Configuring store opening times */}
            <StoreOpeningTimesConfig />
            {/* Displaying list of bikes of the store */}
            <BikeList />
            {/* Single line text field for store name */}
            <SingleLineTextField value={store.name} />
        </div>
    );
};

export default StoreConfigPage;