import React from "react";
import { View, Text, StyleSheet, Image, ScrollView} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import CustomerInput from "../../components/CustomersInput";
import BackButton from "../../components/BackButton/backButton";

import AppletBox from "../../components/AppletsBox/appletBox";

const ChooseServices = () => {
    const Navigation = useNavigation();

    const AppletsHome = () => {
        Navigation.navigate("Applets");
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Text style={styles.homeTitle}>Choose Services</Text>
            <BackButton
            text={"<"}
            onPress={AppletsHome}
            />

            <CustomerInput
            placeholder="Search Services"
            />

            <AppletBox
            title={'test'}
            description={"ok"}
            bgColor={"red"}
            />
            
    </ScrollView>
    )
}

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 80,
        marginLeft: 150,
    },
    section: {
        alignItems: 'center',
        marginVertical: 20,
    },
    ifThisContainer: {
        flexDirection: 'row',
        // alignItems: 'center',
        position: 'relative',  // To contain the absolutely positioned add button
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
    },
    ifThisButton: {
        width: 250,   // Adjust the width for "If This" button
        height: 50,   // Adjust the height for "If This" button
    },
    addButtonContainer: {
        position: 'absolute',
        right: 10,    // Adjust this to place it within the "If This" button visually
        // top: 1,      // Adjust to vertically align
        width: 60,
        borderRadius: 80,
    },
    addButton: {
        paddingHorizontal: 10,
        paddingVertical: 5,
    }
})

export default ChooseServices