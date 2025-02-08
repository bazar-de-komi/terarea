import React from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation, useRoute } from "@react-navigation/native";

import CustomerButton from "../../../components/CustomerButton";
import BackButton from "../../../components/BackButton/backButton";

const Create = () => {
    const navigation = useNavigation();
    const route = useRoute();

    const { action, trigger } = route.params || {};


    const AppletsHome = () => {
        navigation.navigate("Applets");
    };

    const ChooseServices = () => {
        navigation.navigate("Choose services");
        console.log("Trigger dans CreateEnd.js :", trigger);
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
                        text="If"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                    />
                    <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseServices}
                    >
                    <Text style={styles.addButtonText}>
                        {trigger?.json?.name || "Name of the trigger selected"}
                    </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.ThenThatContainer}>
                    <CustomerButton
                        text="Then"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                    />
                    <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseServices}
                    >
                    <Text style={styles.addButtonText}>
                        {action?.json?.name || "Name of the action selected"}
                    </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.ContinueContainer}>
                    <CustomerButton
                        text="Create"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                    />
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
    ContinueContainer: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        width: 300,
        height: 70,
        backgroundColor: 'black',
        borderRadius: 35,
        top: 50,
    },
    ifThenText: {
        fontSize: 24,
        fontWeight: 'bold',
        marginRight: 10,
    },
    addButtonContainer: {
        width: 120,
        height: 50,
        borderRadius: 15,
        backgroundColor: 'white',
        justifyContent: 'center',
        alignItems: 'center',
        right: 30,
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
