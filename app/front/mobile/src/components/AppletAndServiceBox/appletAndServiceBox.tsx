import React from 'react';
import { Text, StyleSheet, TouchableOpacity } from 'react-native';

const AppletAndServiceBox = ({ title, description, bgColor, onPress }) => {
    if (description) {
        return (
            <TouchableOpacity onPress={onPress} style={[styles.boxContainer, { backgroundColor: bgColor }]}>
                <Text style={styles.title}>
                    {title}
                </Text>
                <Text style={styles.description}>
                    {description}
                </Text>
            </TouchableOpacity>
        );
    }
    return (
        <TouchableOpacity onPress={onPress} style={[styles.serviceBoxContainer, { backgroundColor: bgColor }]}>
            <Text style={styles.serviceTitle}>
                {title}
            </Text>
        </TouchableOpacity>
    );
}

const styles = StyleSheet.create({
    boxContainer: {
        flexDirection: "column",
        justifyContent: "center",
        width: '90%',
        paddingTop: 105,
        borderRadius: 20,
        marginBottom: 20,
        alignSelf: 'center'
    },
    serviceBoxContainer: {
        flexDirection: "column",
        justifyContent: "center",
        width: '90%',
        paddingTop: 50,
        borderRadius: 20,
        marginBottom: 20,
        alignSelf: 'center'
    },
    title: {
        bottom: 80,
        fontSize: 28,
        fontWeight: 'bold',
        marginBottom: 40,
        textAlign: 'center',
        color: 'white',
        padding: 10
    },
    serviceTitle: {
        color: "black",
        textAlign: 'center',
        justifyContent: "center",
        alignItems: "center",
        fontWeight: 'bold',
        fontSize: 28,
        marginBottom: 60,
        paddingVertical: 30,
        paddingHorizontal: 10
    },
    description: {
        bottom: 60,
        fontSize: 20,
        marginBottom: 10,
        textAlign: 'center',
        color: 'white',
        padding: 10
    }
});

export default AppletAndServiceBox;
