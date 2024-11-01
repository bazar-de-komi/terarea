import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';

const AppletAndServiceBox = ({ title, description, author, user_nb, bgColor, onPress }) => {
    if (description) {
        return (
            <TouchableOpacity onPress={onPress} style={[styles.boxContainer, { backgroundColor: bgColor }]}>
                <Text style={styles.title}>
                    {title}
                </Text>
                <Text style={styles.description}>
                    {description}
                </Text>
                <View style={styles.boxFooter}>
                    <Text style={styles.textFooter}>
                        by {author}
                    </Text>
                    <View style={styles.userNumberContainer}>
                        <Text style={styles.userImage}>
                            I
                        </Text>
                        <Text style={styles.textFooter}>
                            {user_nb}
                        </Text>
                    </View>
                </View>
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
        color: 'black',
        marginBottom: 10,
        textAlign: 'center',
        color: 'white',
        padding: 10
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
    boxFooter: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        marginHorizontal: 10,
        padding: 10
    },
    textFooter: {
        textAlign: "center",
        color: "white"
    },
    userNumberContainer: {
        flexDirection: "row",
        padding: 10,
    },
    userImage: {
        paddingHorizontal: 10
    }
});

export default AppletAndServiceBox;
