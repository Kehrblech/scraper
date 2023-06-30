import { Component, EventEmitter, OnInit, Output, ViewChild, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../api-service/api-service.component';
import { MatSnackBar } from '@angular/material/snack-bar';


@Component({
  selector: 'app-start-page',
  templateUrl: './start-page.component.html',
  styleUrls: ['./start-page.component.css'],
})
export class StartPageComponent implements OnInit {
  searchPhrase: string = '';
  isEntrySuccessful: boolean = false;
  @ViewChild("searchInput") searchInput!: ElementRef<HTMLInputElement>;
  @Output() entrySuccessful: EventEmitter<boolean> = new EventEmitter<boolean>();
  constructor(
    private router: Router,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {}

  focusSearchInput(){
    this.searchInput.nativeElement.focus();
  }


  fetchSlides() {
    this.apiService.getUrl(this.searchPhrase).subscribe(
      (result: Object) => {
        if (result === 0 || result === 1) {
          // Show snackbar with Error Message
          this.snackBar.open('Error fetching slides.', 'Close', {
            duration: 3000,
          });
          this.isEntrySuccessful = false;
        } else {
          const url = result as string;
          this.router.navigate(['/slideshow'], { queryParams: { url: url } });
          this.isEntrySuccessful = true;
        }
      },
      (error) => {
        // Show snackbar with Error Message
        this.snackBar.open('An error occurred.', 'Close', {
          duration: 3000,
        });
        this.isEntrySuccessful = false;
      }
    );
    this.entrySuccessful.emit(this.isEntrySuccessful);
  }
}
