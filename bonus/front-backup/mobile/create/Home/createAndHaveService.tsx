import React, { useEffect } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation, useRoute } from "@react-navigation/native";

import CustomButton from "../../../components/CustomButton/customButton";
import Header from "../../../components/Header/header";

const CreateHaveService = () => {
    const navigation = useNavigation();
    const route = useRoute();
    const { trigger } = route.params || {};

    const ChooseServices = () => {
        navigation.navigate("Choose options service for action", { trigger });
    };

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header />
            <Text style={styles.homeTitle}>Create</Text>
            <View style={styles.section}>
                <View style={styles.ifThisContainer}>
                    <CustomButton
                        text="If This"
                        type="PRIMARY"
                        bgColor={"black"}
                        fgColor={"white"}
                        onPress={null}
                        icon={null}
                    />
                    <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseServices}
                    >
                        <Text style={styles.addButtonText}>
                            {trigger.name || "Name of the action selected"}
                        </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.ThenThatContainer}>
                    <CustomButton
                        text="Then That"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        onPress={null}
                        icon={null}
                    />
                    <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseServices}
                    >
                        <Text style={styles.addButtonText}>add</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 40,
        fontWeight: 'bold',
        marginTop: 60,
        marginBottom: 50,
        textAlign: 'center'
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

export default CreateHaveService;
