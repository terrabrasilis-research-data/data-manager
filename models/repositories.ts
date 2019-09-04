declare module repositories {

    export interface User {
        name: string;
        image: string;
    }

    export interface Service {
        id: number;
        name: string;
        host: string;
        ports: number[];
        created_on: Date;
    }

    export interface CustomField {
    }

    export interface Repositorie {
        id: number;
        name: string;
        abstract: string;
        maintainer: string;
        created_on: Date;
        language: string;
        email: string;
        bbox: number[];
        keywords: string[];
        categories: string[];
        users: User[];
        services: Service[];
        custom_fields: CustomField[];
    }

}