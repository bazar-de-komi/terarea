import React, { useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { useNavigation } from "@react-navigation/native";

import BackButton from "../../components/BackButton/backButton";

const ActionPage = () => {
    const [selectedHour, setSelectedHour] = useState("12 AM");
    const [selectedMinute, setSelectedMinute] = useState("00");

    const navigation = useNavigation();

    const AppletsHome = () => {
        navigation.navigate("Applets");
    };

    const End = () => {
        navigation.navigate("Create end");
    };

    const hours = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
                   "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"];
    
                   const minutes = Array.from({ length: 60 }, (_, i) => (i < 10 ? `0${i}` : `${i}`));

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Complete action fields</Text>
            <Text style={styles.description}>Send an email</Text>
            
            <View style={styles.backButtonContainer}>
                <BackButton
                    text={"BACK"}
                    onPress={AppletsHome}
                />
            </View>
            <Text style={styles.label}>Time</Text>
            
            <View style={styles.pickerContainer}>
                <Picker
                    selectedValue={selectedHour}
                    style={styles.picker}
                    onValueChange={(itemValue) => setSelectedHour(itemValue)}
                >
                    {hours.map((hour) => (
                        <Picker.Item key={hour} label={hour} value={hour} />
                    ))}
                </Picker>
            </View>

            <View style={styles.pickerContainer}>
                <Picker
                    selectedValue={selectedMinute}
                    style={styles.picker}
                    onValueChange={(itemValue) => setSelectedMinute(itemValue)}
                >
                    {minutes.map((minute) => (
                        <Picker.Item key={minute} label={minute} value={minute} />
                    ))}
                </Picker>
            </View>

            <TouchableOpacity
                style={styles.triggerButton}
                onPress={End} >
                <Text style={styles.triggerButtonText}>Create action</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        top: 20,
        flex: 1,
        backgroundColor: "#333",
        paddingHorizontal: 20,
        paddingVertical: 40,
        alignItems: "center",
    },
    backButtonContainer: {
        left: 160,
        marginTop: -60,
        marginBottom: 100,
    },
    title: {
        fontSize: 30,
        fontWeight: "bold",
        color: "white",
        marginBottom: 10,
    },
    description: {
        fontSize: 16,
        color: "#bbb",
        textAlign: "center",
        marginBottom: 30,
    },
    label: {
        fontSize: 18,
        fontWeight: "600",
        color: "white",
        alignSelf: "flex-start",
        marginBottom: 10,
    },
    pickerContainer: {
        width: "100%",
        backgroundColor: "white",
        borderRadius: 8,
        marginBottom: 15,
        overflow: "hidden",
    },
    picker: {
        height: 50,
        color: "black",
    },
    triggerButton: {
        marginTop: 30,
        backgroundColor: "white",
        paddingVertical: 15,
        paddingHorizontal: 30,
        borderRadius: 25,
        width: "100%",
        alignItems: "center",
    },
    triggerButtonText: {
        fontSize: 18,
        fontWeight: "bold",
        color: "#333",
    },
});

export default ActionPage;