import React, { useState } from "react";
import { View, Text, TextInput, StyleSheet, TouchableOpacity } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { useNavigation } from "@react-navigation/native";

const jsonData = {
    "name": "Every day",
    "description": "This action triggers every day at a specific time set by you.",
    "service": {
        "url_params": {
            "drop:timeZone": [
                "opt:Africa/Cairo", "opt:America/New_York", "default:Europe/Paris"
            ]
        },
        "verification": {
            "hour": {
                "drop:verification_value": [
                    "default:0", "opt:1", "opt:2", "opt:3"
                ]
            },
            "minute": {
                "drop:verification_value": [
                    "default:0", "opt:10", "opt:20", "opt:30"
                ]
            }
        }
    }
};

const parseJsonToForm = (json) => {
    const fields = [];
    
    const traverse = (obj, parentKey = "") => {
        Object.entries(obj).forEach(([key, value]) => {
            if (key.startsWith("ignore:")) return;
            
            if (key.startsWith("drop:")) {
                const fieldName = key.replace("drop:", "");
                const options = value.map(option => option.replace(/^(opt:|default:)/, ""));
                fields.push({ type: "dropdown", name: fieldName, options });
            } else if (typeof value === "object" && !Array.isArray(value)) {
                traverse(value, key);
            } else {
                fields.push({ type: "input", name: key, defaultValue: value });
            }
        });
    };
    traverse(json);
    return fields;
};

const TriggerPage = () => {
    const Navigation = useNavigation();
    const formFields = parseJsonToForm(jsonData);
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
                    
                    {field.type === "dropdown" ? (
                        <Picker
                            selectedValue={formValues[field.name] || field.options[0]}
                            style={styles.picker}
                            onValueChange={(itemValue) => handleChange(field.name, itemValue)}
                        >
                            {field.options.map((option, idx) => (
                                <Picker.Item key={idx} label={option} value={option} />
                            ))}
                        </Picker>
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
