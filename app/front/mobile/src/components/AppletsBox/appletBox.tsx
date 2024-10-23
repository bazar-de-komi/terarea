import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const AppletBox = ({title, description, bgColor, onPress}) => {
    return (
        <TouchableOpacity onPress={onPress}>
            <View style={[styles.boxContainer, { backgroundColor: bgColor}]}>
                <Text style={styles.title}>{title}</Text>
                <Text style={styles.description}>{description}</Text>
            </View>
        </TouchableOpacity>
    );
}
const styles = StyleSheet.create({
    boxContainer: {
        width: '90%',
        // height: '50%',
        padding: 105,
        borderRadius: 20,
        marginBottom: 20,
        alignSelf: 'center',
    },
    title: {
        bottom: 80,
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 40,
        textAlign: 'left',
    },
    description: {
        bottom: 80,
        fontSize: 14,
        color: 'black',
        marginBottom: 10,
    },
    tagsContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
    },
    tag: {
        backgroundColor: '#ddd',
        borderRadius: 15,
        padding: 5,
        marginRight: 10,
        marginBottom: 10,
    },
    tagText: {
        fontSize: 12,
        color: '#333',
    },
});

export default AppletBox;