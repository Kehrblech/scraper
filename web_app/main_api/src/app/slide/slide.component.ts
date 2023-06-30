import { Component, Input } from '@angular/core';
import { Clipboard } from '@angular/cdk/clipboard';
import { MatSnackBar } from '@angular/material/snack-bar';
interface SlideContent {
  type: string;
  value: string;
  // Add more properties if necessary
}

@Component({
  selector: 'app-slide',
  templateUrl: './slide.component.html',
  styleUrls: ['./slide.component.css']
})
export class SlideComponent {
  @Input() slideData: any;
  isFirstImage: boolean = true;
  currentIndex = 0;
  constructor(private clipboard: Clipboard, private snackBar: MatSnackBar) { }


  splitTextSentences(text: string): string[] {
    const sentences = text.split(/(?<![0-9])\. /);
    const formattedSentences = sentences.map(sentence => sentence.trim() + '.');
    return formattedSentences;
  }

  splitImageSentences(url: string) {
    url = url.replace("/thumb", "");
    url = url.replace(/\.svg.*/, ".svg");

    return url
  }

  nextImage() {
    this.currentIndex++;
    // Überprüfe, ob der Index das Ende der Bilder erreicht hat
    if (this.currentIndex >= this.slideData.text.length - 1) {
      // Setze den Index auf 0, um zum Anfang zurückzukehren
      this.currentIndex = 0;
    }
  }
  lastImage() {
    this.currentIndex--;
    console.log(this.currentIndex)
    // Überprüfe, ob der Index das Ende der Bilder erreicht hat
    if (this.currentIndex < 0) {
      // Setze den Index auf 0, um zum Anfang zurückzukehren
      this.currentIndex = this.slideData.text.length - 2;
      console.log(this.currentIndex)
    }
  }

  // In der zugehörigen Komponentenklasse
  getNumberOfImages(): number {
    return this.slideData.text.filter((content: any) => content.type === 'image').length;
  }

  copySlideToClipboard(slideData: any) {
    const currentSlide = JSON.stringify(slideData, null, 2);
    this.clipboard.copy(currentSlide);
    this.snackBar.open('Slide copied to clipboard!', 'OK', {
      duration: 2000,
    });
  }

  getSlideText(slide: any): string {
    if (slide && slide.mainTitle && slide.title && slide.text) {
      const mainTitle = slide.mainTitle;
      const title = slide.title;
      const textContent = slide.text.map((content: any) => content.value).join('\n');

      return `Main Title: ${mainTitle}\nTitle: ${title}\nContent: ${textContent}`;
    } else {
      // Handle den Fall, wenn das slide-Objekt nicht die erwarteten Eigenschaften enthält
      return '';
    }
  }

}
