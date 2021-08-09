import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-progress',
  templateUrl: './progress.component.html',
  styleUrls: ['./progress.component.scss']
})
export class ProgressComponent implements OnInit {
  @Input() showSpinner = false;
  @Input() percent = 0;
  title = 'ngrx';
  constructor() {}

  ngOnInit() {}
}
