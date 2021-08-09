import {Component, ViewChild, ElementRef, OnInit} from '@angular/core';
import {ConnectionsService} from './Services/connections.service';
import {HttpEventType, HttpResponse} from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  @ViewChild('fileDropRef', {static: false}) fileDropEl: ElementRef;
  files: any[] = [];
  showSpinner = false;
  showButton = false;

  constructor(private connectionService: ConnectionsService) {
  }

  ngOnInit() {
    this.connectionService.init().subscribe();
  }

  /**
   * on file drop handler
   */
  onFileDropped($event) {
    this.prepareFilesList($event);
  }

  /**
   * handle file from browsing
   */
  fileBrowseHandler(files) {
    this.prepareFilesList(files);
  }

  /**
   * Delete file from files list
   * @param index (File index)
   */
  deleteFile(index: number) {
    if (this.files[index].progress < 100) {
      console.log('Upload in progress.');
      return;
    }
    this.files.splice(index, 1);
  }

  /**
   * Simulate the upload process
   */
  uploadFilesSimulator(index: number, files = null) {
    console.log(index)
    this.connectionService.upload(this.files[index]).subscribe(
      (event: any) => {
        if (event.type === HttpEventType.UploadProgress) {
          this.files[index].progress = Math.round(100 * event.loaded / event.total);
          if (this.files[index].progress === 100 && index < this.files.length - 1) {
            this.uploadFilesSimulator(index + 1);
          }
        } else if (event instanceof HttpResponse) {
          console.log(event);
        }
      },
      (err: any) => {
        console.log(err);
      }
    );
  }

  /**
   * Convert Files list to normal array list
   * @param files (Files List)
   */
  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      item.progress = 0;
      this.files.push(item);
    }
    this.fileDropEl.nativeElement.value = '';
    this.showButton = true;
    // this.uploadFilesSimulator(0, this.files);
  }

  /**
   * format bytes
   * @param bytes (File size in bytes)
   * @param decimals (Decimals point)
   */
  formatBytes(bytes, decimals = 2) {
    if (bytes === 0) {
      return '0 Bytes';
    }
    const k = 1024;
    const dm = decimals <= 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  uploadFiles() {
    this.uploadFilesSimulator(0);
  }
}
