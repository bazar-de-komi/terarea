import React from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../../components/CustomerButton";
import BackButton from "../../../components/BackButton/backButton";

const Create = () => {
    const navigation = useNavigation();

    const AppletsHome = () => {
        navigation.navigate("Applets");
    };

    const ChooseServices = () => {
        navigation.navigate("Choose options service for trigger");
    };

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Text style={styles.homeTitle}>Create</Text>
            <View style={styles.backButtonContainer}>
                <BackButton
                    text={"X"}
                    onPress={AppletsHome}
                />
            </View>
            <View style={styles.section}>
                <View style={styles.ifThisContainer}>
                    <CustomerButton
                        text="If This"
                        type="PRIMARY"
                        bgColor={"black"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                    />
                    <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseServices}
                    >
                    <Text style={styles.addButtonText}>add</Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.ThenThatContainer}>
                    <CustomerButton
                        text="Then That"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                    />
                    {/* <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseServices}
                    >
                    <Text style={styles.addButtonText}>add</Text>
                    </TouchableOpacity> */}
                </View>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 40,
        fontWeight: 'bold',
        margin: 80,
        marginLeft: 140,
        justifyContent: 'center',
        alignItems: 'center',
    },
    section: {
        alignItems: 'center',
    },
    ifThisContainer: {
        flexDirection: 'row',
        position: 'relative',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 80,
        width: 300,
        height: 70,
        backgroundColor: 'black',
        borderRadius: 35,
        paddingHorizontal: 15,
    },
    ThenThatContainer: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
        width: 300,
        height: 70,
        backgroundColor: 'grey',
        borderRadius: 35,
    },
    ifThenText: {
        fontSize: 24,
        fontWeight: 'bold',
        marginRight: 10,
    },
    addButtonContainer: {
        width: 60,
        height: 30,
        borderRadius: 15,
        backgroundColor: 'white',
        justifyContent: 'center',
        alignItems: 'center',
    },
    addButtonText: {
        color: 'black',
        fontSize: 14,
        fontWeight: 'bold',
    },
    backButtonContainer: {
        left: 160,
        marginTop: -60,
        marginBottom: 100,
    },
});

export default Create;
