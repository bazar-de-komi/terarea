import React from "react";
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../components/CustomersInput";
import BackButton from "../../components/BackButton/backButton";

import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";

const ChooseServices = () => {
    const Navigation = useNavigation();

    const AppletsHome = () => {
        Navigation.navigate("Applets");
    }

    const createTwo = () => {
        Navigation.navigate("Create two");
    }

    const dateTimeTrigger = () => {
        Navigation.navigate("Date time trigger");
    }

    const chooseOption = () => {
        Navigation.navigate("Choose options");
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <BackButton 
            text={"back"}
            onPress={AppletsHome}
            />
            <Text style={styles.homeTitle}>Choose a trigger</Text>

            <View style={styles.searchContainer}>
                <CustomerInput
                    placeholder="Search Services"
                    style={styles.searchInput}
                />
            </View>

            <AppletAndServiceBox
                title={'title'}
                description={"description"}
                bgColor={"red"}
                onPress={dateTimeTrigger}
                // onPress={choose }
            />

        </ScrollView>
    )
}

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 80,
        marginLeft: 100,
    },
    searchContainer: {
        alignItems: 'center',
        marginVertical: 10,
    },
    searchInput: {
        width: '80%',
    },
    section: {
        alignItems: 'center',
        marginVertical: 20,
    },
    ifThisContainer: {
        flexDirection: 'row',
        position: 'relative',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
    },
    ifThisButton: {
        width: 250,
        height: 50,
    },
    addButtonContainer: {
        position: 'absolute',
        right: 10,
        width: 60,
        borderRadius: 80,
    },
    addButton: {
        paddingHorizontal: 10,
        paddingVertical: 5,
    }
})

export default ChooseServices
