import React, { useState } from "react";
import { View, Text, TextInput, StyleSheet, TouchableOpacity } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { useNavigation } from "@react-navigation/native";
import ParseJson from "../../ParseJson.js";

const jsonData = {
    "": "Ceci est un texte affiché",
    "ignore:ceChamp": "Ne pas afficher",
    "drop:choixPays": [
        "default:France",
        "opt:USA",
        "opt:Canada",
    ],
    "input:nom": "Jean Dupont",
    "textarea:description": "Texte long ici...",
    "service": {
        "drop:timeZone": [
            "opt:Africa/Cairo",
            "opt:America/New_York",
            "default:Europe/Paris"
        ],
        "verification": {
            "drop:hour": [
                "default:0",
                "opt:1",
                "opt:2",
                "opt:3"
            ],
            "drop:minute": [
                "default:0",
                "opt:10",
                "opt:20",
                "opt:30"
            ]
        }
    }
};

const TriggerPage = () => {
    const Navigation = useNavigation();
    const formFields = ParseJson(jsonData);
    const [formValues, setFormValues] = useState({});

    const handleChange = (name, value) => {
        setFormValues(prev => ({ ...prev, [name]: value }));
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Complete trigger fields</Text>
            
            {formFields.map((field, index) => (
                <View key={index} style={styles.fieldContainer}>
                    <Text style={styles.label}>{field.name}</Text>

                    {field.type === "text" ? (
                        <Text style={styles.text}>{field.value}</Text>
                    ) : field.type === "dropdown" ? (
                        <Picker
                            selectedValue={formValues[field.name] || field.defaultValue}
                            style={styles.picker}
                            onValueChange={(itemValue) => handleChange(field.name, itemValue)}
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
                            onChangeText={(text) => handleChange(field.name, text)}
                        />
                    ) : (
                        <TextInput
                            style={styles.input}
                            defaultValue={field.defaultValue}
                            onChangeText={(text) => handleChange(field.name, text)}
                        />
                    )}
                </View>
            ))}

            <TouchableOpacity
                style={styles.triggerButton}
                onPress={() => console.log("Form Values:", formValues)}
            >
                <Text style={styles.triggerButtonText}>Create trigger</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#333",
        paddingHorizontal: 20,
        paddingVertical: 40,
        alignItems: "center",
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

export default TriggerPage;
