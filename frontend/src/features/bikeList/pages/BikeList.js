import React from "react";
import { useTranslation } from 'react-i18next';


import './BikeList.css'
import BikeListItem from '../components/BikeListItem'

const BikeList = () => {

    const { t } = useTranslation();

    // TODO: implement fetching
    let bikes = [
        {
            id: "1",
            name: "Lastenrad 1"
        },
        {
            id: "2",
            name: "Lastenrad 2"
        },
        {
            id: "3",
            name: "Lastenrad 3"
        },
    ]

    // FIXME: hover response of all buttons

    return (
        <>
            <h1>Heading</h1>

            <ul>
                <li className="list">
                    {bikes.map((bike) => (
                        <BikeListItem bike={bike} key={bike.id}/>
                    ))}
                </li>
            </ul>
        </>
    );
};
  
export default BikeList;