import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  constructor(private router: Router) {}

  title = 'main_api';
  isDrawerOpened = false;
  isEntrySuccessful: boolean = false;

  toggleDrawer() {
    this.isDrawerOpened = !this.isDrawerOpened;
  }

  navigateToSlideshow() {
    this.router.navigate(['/slideshow']);
  }

}
