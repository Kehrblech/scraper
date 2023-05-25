import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-input-bar',
  templateUrl: './input-bar.component.html',
  styleUrls: ['./input-bar.component.css']
})
export class InputBarComponent {
  inputValue: string = '';

  constructor(private http: HttpClient) { }

  simpleRequest(value: string) {
    const apiUrl = 'http://localhost:5000/'+value;
    // const params = {query: value};

    this.http.get(apiUrl).subscribe(
      (response) => {
        // Handle the API response here
        console.log(response);
      },
      (error) => {
        // Handle any API errors here
        console.error(error);
      }
    );
  }

}
