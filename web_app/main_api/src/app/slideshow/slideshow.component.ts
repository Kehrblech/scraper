import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../api-service/api-service.component';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
interface SlideContent {
  type: string;
  value: string;
  imageUrl?: string; // optional property for image URLs
}

interface Slide {
  mainTitle: string;
  text: SlideContent[];
}

@Component({
  selector: 'app-slideshow',
  templateUrl: './slideshow.component.html',
  styleUrls: ['./slideshow.component.css']
})
export class SlideShowComponent implements OnInit {
  slides: Slide[] = [];
  isLoading: boolean = false;
  currentSlideIndex: number = 0;
  url: string = '';
  isFullscreen = false;


  constructor(private route: ActivatedRoute, private apiService: ApiService) { }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      const url = params['url'];
      if (url) {
        this.fetchData(url);
      }
    });
  }

  toggleFullscreen() {
    this.isFullscreen = !this.isFullscreen;
  }



  fetchData(url: string) {
    this.isLoading = true;
    this.apiService.getData(url).subscribe((data: any) => {
      console.log(data);

      this.slides = this.convertJsonToSlides(data);
      this.isLoading = false;
    });
  }

  convertJsonToSlides(data: any): Slide[] {
    const slides: Slide[] = [];

    for (const slideData of data.slides) {
      const slide: Slide = {
        mainTitle: slideData.name,
        text: []
      };

      if (slideData.images && slideData.images.length > 0 && slideData.text && slideData.text.length > 0){
        for (const image of slideData.images) {
          const imageUrl = image.url;
          slide.text.push({ type: 'image', value: imageUrl, imageUrl });
        }
        const textValue = Array.isArray(slideData.text) ? slideData.text.join(' ') : slideData.text;
        slide.text.push({ type: 'text', value: textValue });
        slides.push(slide);
      }

    }

    return slides;
  }

  nextSlide() {
    this.currentSlideIndex = (this.currentSlideIndex + 1) % this.slides.length;
  }
  lastSlide() {
    this.currentSlideIndex = (this.currentSlideIndex - 1) % this.slides.length;
  }
}


