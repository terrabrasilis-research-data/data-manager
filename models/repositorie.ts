declare module repositories {

    export interface User {
        id: number;
        name: string;
        image: string;
    }

    export interface CustomField {
    }

    export interface Service {
        id: number;
        name: string;
        host: string;
        ports: number[];
        created_on: Date;
    }

    export interface Repositorie {
        id: number;
        name: string;
        users: User[];
        abstract: string;
        categories: string[];
        keywords: string[];
        maintainer: string;
        language: string;
        created_on: Date;
        services: Service[];
        email: string;
        bbox: number[];
        custom_fields: CustomField[];
    }

}