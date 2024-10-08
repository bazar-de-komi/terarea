import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const AppletBox = ({title, description, bgColor}) => {
    return (
        <View style={[styles.boxContainer, { backgroundColor: bgColor}]}>
            <Text style={styles.title}>{title}</Text>
            <Text style={styles.description}>{description}</Text>
            {/* <View style={styles.tagsContainer}>
                {tags.map((tag, index) => (
                    <View key={index} style={styles.tag}>
                        <Text style={styles.tagText}>{tag}</Text>
                    </View> */}
                {/* ))} */}
            {/* </View> */}
        </View>
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