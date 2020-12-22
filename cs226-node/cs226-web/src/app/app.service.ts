import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AppService {
  apiUrl: string = environment.apiUrl + 'cities';
  constructor(private http: HttpClient) { }

  getCities(params): Observable<any> {
    return this.http.get(this.apiUrl, { params: params });
  }
}
