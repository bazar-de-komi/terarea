import React from 'react';
import { Text, StyleSheet, TouchableOpacity } from 'react-native';

const BackButton = ({ text, onPress }) => {
    return (
        <TouchableOpacity onPress={onPress} style={styles.backStyle}>
            <Text style={styles.buttonText}>
                {text}
            </Text>
        </TouchableOpacity>
    );
}
const styles = StyleSheet.create({
    backStyle: {
        right: 0,
        top: 10,
        paddingHorizontal: 20,
        paddingVertical: 10
    },
    buttonText: {
        fontSize: 20,
        fontWeight: "bold"
    }
});

export default BackButton;
