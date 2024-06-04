import React from "react";
import { useTranslation } from 'react-i18next';


import './BikeList.css'
import BikeListItem from '../components/BikeListItem'

const BikeList = () => {

    const { t } = useTranslation();

    // TODO: implement fetching
    let bikes = [
        {
            name: "Lastenrad 1"
        },
        {
            name: "Lastenrad 2"
        },
        {
            name: "Lastenrad 3"
        },
    ]

    return (
        <>
            <ul>
                <li className="list">
                    {bikes.map((bike, index) => (
                        <BikeListItem bike={bike} key={index}/>
                    ))}
                </li>
            </ul>
        </>
    );
};
  
export default BikeList;