import React, { useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { useNavigation, useRoute } from "@react-navigation/native";
import { parseJsonToForm, injectFormValuesIntoJson } from "../../Parsing/ParseJson";

import BackButton from "../../components/BackButton/backButton";
import CustomerInput from "../../components/CustomersInput";

const ActionPage = () => {
    const navigation = useNavigation();
    const route = useRoute();
    const { service, trigger, action } = route.params || {};

    const AppletsHome = () => {
        navigation.navigate("Applets");
    };

    const goToCreateEnd = () => {
        const updatedAction = injectFormValuesIntoJson(action.json, formValues);
        navigation.navigate("Create end", { trigger: trigger, action: updatedAction, service: service });
    };

    const formFields = parseJsonToForm(action.json);
    const [formValues, setFormValues] = useState(formFields);

    const handleChange = (name, keyToChange, value) => {
        setFormValues((prev) =>
            prev.map((item) =>
                item.name === name ? { ...item, [keyToChange]: value } : item
            )
        );
    };

    return (
        <ScrollView showsVerticalScrollIndicator={true} style={styles.container}>
            <Text style={styles.title}>Complete action fields</Text>
            {formFields.map((field, index) => (
                <View key={index} style={styles.fieldContainer}>
                    <Text style={styles.label}>{field.name}</Text>

                    {field.type === "text" ? (
                        <Text style={styles.text}>{field.value}</Text>
                    ) : field.type === "dropdown" ? (
                        <Picker
                            selectedValue={formValues.find(f => f.name === field.name)?.defaultValue ?? field.defaultValue}
                            style={styles.picker}
                            onValueChange={(itemValue) => handleChange(field.name, "defaultValue", itemValue)}
                        >
                            {field.options.map((option, idx) => (
                                <Picker.Item key={idx} label={option} value={option} />
                            ))}
                        </Picker>
                    ) : field.type === "textarea" ? (
                        <TextInput
                            style={styles.textarea}
                            defaultValue={field.defaultValue}
                            multiline={true}
                            onChangeText={(text) => handleChange(field.name, "value", text)}
                        />
                    ) : (
                        <TextInput
                            style={styles.input}
                            defaultValue={field.defaultValue}
                            onChangeText={(text) => handleChange(field.name, "value", text)}
                        />
                    )}
                </View>
            ))}

            <TouchableOpacity style={styles.triggerButton} onPress={goToCreateEnd} >
                <Text style={styles.triggerButtonText}>Create action</Text>
            </TouchableOpacity>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#333",
        paddingHorizontal: 20,
        paddingVertical: 40,
    },
    title: {
        fontSize: 24,
        fontWeight: "bold",
        color: "white",
        marginBottom: 20,
    },
    fieldContainer: {
        width: "100%",
        marginBottom: 15,
    },
    label: {
        fontSize: 18,
        fontWeight: "600",
        color: "white",
        marginBottom: 5,
    },
    text: {
        fontSize: 16,
        color: "white",
    },
    picker: {
        backgroundColor: "white",
        borderRadius: 8,
    },
    input: {
        backgroundColor: "white",
        borderRadius: 8,
        padding: 10,
        fontSize: 16,
    },
    textarea: {
        backgroundColor: "white",
        borderRadius: 8,
        padding: 10,
        fontSize: 16,
        height: 100,
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
