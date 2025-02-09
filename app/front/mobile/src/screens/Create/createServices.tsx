import React, { useState } from "react";
import { View, Text, TextInput, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import BackButton from "../../components/BackButton/backButton";

const CreateServices = () => {
    const navigation = useNavigation();
    const [serviceName, setServiceName] = useState("");
    const [serviceType, setServiceType] = useState("Option 1");
    const [startDate, setStartDate] = useState("03/11/2024");
    const [startTime, setStartTime] = useState("-- : --");
    const [username, setUsername] = useState("");
    const [age, setAge] = useState("0");

    const AppletsHome = () => {
        navigation.navigate("Applets");
    };

    const ChooseServices = () => {
        navigation.navigate("Choose services");
    };

    return (
        <ScrollView showsVerticalScrollIndicator={false} style={styles.container}>
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
                        bgColor={"black"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                    />
                    <View style={styles.addButtonContainerIf}>
                        <Text style={styles.addButtonTextIf}>
                            {serviceName || "No service selected"}
                        </Text>
                    </View>
                </View>

                <View style={styles.infoBox}>
                    <Text style={styles.infoBoxTitle}>Title</Text>
                    <Text style={styles.infoBoxDescription}>Description</Text>

                    <Text style={styles.label}>ServiceType:</Text>
                    <Picker
                        selectedValue={serviceType}
                        onValueChange={(itemValue) => setServiceType(itemValue)}
                        style={styles.picker}
                    >
                        <Picker.Item label="Option 1" value="Option 1" />
                        <Picker.Item label="Option 2" value="Option 2" />
                        <Picker.Item label="Option 3" value="Option 3" />
                    </Picker>

                    <Text style={styles.label}>StartDate:</Text>
                    <TextInput
                        style={styles.input}
                        value={startDate}
                        editable={false}
                    />

                    <Text style={styles.label}>StartTime:</Text>
                    <TextInput
                        style={styles.input}
                        value={startTime}
                        placeholder="-- : --"
                        editable={false}
                    />

                    <Text style={styles.label}>Username:</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Enter Username"
                        value={username}
                        onChangeText={setUsername}
                    />

                    <Text style={styles.label}>Age:</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="0"
                        keyboardType="numeric"
                        value={age}
                        onChangeText={setAge}
                    />
                </View>

                <View style={styles.ThenThatContainer}>
                    <CustomerButton
                        text="Then"
                        type="PRIMARY"
                        bgColor={"grey"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                    />
                    <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseServices}
                    >
                        <Text style={styles.addButtonText}>
                            {serviceName || "Add"}
                        </Text>
                    </TouchableOpacity>
                </View>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingHorizontal: 20,
    },
    homeTitle: {
        fontSize: 40,
        fontWeight: 'bold',
        margin: 20,
        textAlign: 'center',
    },
    section: {
        alignItems: 'center',
    },
    ifThisContainer: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
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
        marginVertical: 20,
        width: 300,
        height: 70,
        backgroundColor: 'grey',
        borderRadius: 35,
    },
    ifThenText: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        left:50,
    },
    addButtonContainerIf: {
        justifyContent: 'center',
        alignItems: 'center',
    },
    addButtonTextIf: {
        color: 'white',
        fontSize: 14,
        fontWeight: 'bold',
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
        alignSelf: 'center',
        marginVertical: 20,
    },
    infoBox: {
        width: '100%',
        padding: 20,
        backgroundColor: '#f0f0f0',
        borderRadius: 10,
        marginBottom: 20,
    },
    infoBoxTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 5,
    },
    infoBoxDescription: {
        fontSize: 14,
        color: '#888',
        marginBottom: 20,
    },
    label: {
        fontSize: 14,
        fontWeight: 'bold',
        marginTop: 10,
    },
    picker: {
        backgroundColor: 'white',
        borderRadius: 5,
        marginVertical: 5,
    },
    input: {
        backgroundColor: 'white',
        padding: 10,
        borderRadius: 5,
        marginVertical: 5,
    },
});

export default CreateServices;
