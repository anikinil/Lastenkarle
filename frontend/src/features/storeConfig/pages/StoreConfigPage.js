import React from "react";




const StoreConfigPage = () => {

    return (
        <>
            <h1>{t('new_store')}</h1>
            <PictureAndDescriptionField editable={true} />
            <AddressField editable={true} />
            <StoreOpeningTimesConfig />

            <h2>{t('add_bikes_to_store')}</h2>
            <BikeList />

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleCancelClick}>{t('cancel')}</button>
                <button type='button' className='button accent' onClick={handleRegisterClick}>{t('register_new_store')}</button>
            </div>
        </>
    )
}

export default StoreConfigPage;