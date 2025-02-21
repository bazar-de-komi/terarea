import React, { useState, useEffect } from 'react';
import { View, ActivityIndicator, Button, Alert } from 'react-native';
import { useNavigation } from "@react-navigation/native";
import WebView from 'react-native-webview';
import { deleteKey, storeValue, getValue } from '../../../components/StoreData/storeData';
import { queries } from '../../../../back-endConnection/querier';

export const OAuthScreen = () => {
    const [authUrl, setAuthUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const navigation = useNavigation();

    useEffect(() => {
        const fetchAuthUrl = async () => {
            const url = await getValue("authUrl");
            setAuthUrl(url);
            setLoading(false);
        };

        fetchAuthUrl();
    }, []);

    const onNavigationStateChange = async (event: any) => {
        if (event.url.startsWith("https://pingpal.news/callback")) {
            const urlParams = new URLSearchParams(event.url.split('?')[1]);
            const code = urlParams.get('code');
            if (code) {
                let path: string = "/api/v1/oauth/callback?";
                path += event.url.split('?')[1];
                try {
                    setLoading(true);
                    const response = await queries.post(path);
                    storeValue('token', response.token);
                    await deleteKey("authUrl");
                    setAuthUrl(null);
                    navigation.navigate("All");
                } catch (error) {
                    setLoading(true);
                    console.error(error);
                    Alert.alert("The oauth connexion have failed.");
                    await deleteKey("authUrl");
                    setAuthUrl(null);
                    navigation.goBack();
                };
            };
        };
    };

    if (loading) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <ActivityIndicator size="large" color="#0000ff" />
            </View>
        );
    }

    return (
        <View style={{ flex: 1 }}>
            {authUrl && (
                <WebView
                    source={{ uri: authUrl }}
                    onNavigationStateChange={onNavigationStateChange}
                    userAgent="Mozilla/5.0"
                />
            )}
        </View>
    );
};
