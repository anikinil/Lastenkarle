import React from "react";
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import PictureAndDescriptionField from '../../../components/IO/PictureAndDescriptionField';
import AddressField from '../../../components/IO/AddressField';
import { useParams } from 'react-router-dom';
//Standard page for a specific region
//TODO: Add Map of Region with store markers
//TODO: Add calandar table for bikes in region
//TODO: Add bike list of region
let regions = [
    {
        id: 'karlsruhe',
        name: 'Karlsruhe',
        //bikes: [bikes in this region]
    },
    {
        id: 'ettlingen',
        name: 'Ettlingen',
    },
    {
        id: 'malsch',
        name: 'Malsch',
    },
    {
        id: 'bruchsaal',
        name: 'Bruchsaal'
    }
]

const RegionalBooking = () => {
    const { t } = useTranslation();

    const { id } = useParams();
    const region = regions.find(s => s.id === id);
    return (
        <h1>{region.name}</h1>
    );
};
  
export default RegionalBooking;