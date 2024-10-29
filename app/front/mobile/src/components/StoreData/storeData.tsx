// import React, { useState } from "react";
import AsyncStorage from '@react-native-async-storage/async-storage'

export const storeValue = async (key: string, value: any) => {
    try {
        await AsyncStorage.setItem(key, value);
    } catch (e) {
        console.error(e);
    }
};

export const getValue = async (key: string) => {
    try {
        const value = await AsyncStorage.getItem(key);
        if(value !== null) {
            return value;
        }
    } catch (e) {
        console.error(e);
    }
};

export const deleteKey = async (key: string) => {
    try {
        await AsyncStorage.removeItem(key);
    } catch (e) {
        console.error(e);
    }
};

// export default {
//     storeValue,
//     getValue,
//     deleteKey
// }