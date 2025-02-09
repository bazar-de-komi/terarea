import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

import CustomerButton from '../CustomerButton';

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
        right: 150,
        bottom: 70,
        paddingHorizontal: 20,
        paddingVertical: 10
    },
    buttonText: {
        fontSize: 20,
        fontWeight: "bold"
    }
});

export default BackButton;
